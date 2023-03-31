from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product,Address, Profile, CartDetail, OrderDetail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404
import time
from django.template.response import TemplateResponse
from django.views import View

# Create your views here.
def index(request):
#     num_users = User.objects.raw(
#     # select * from Product
#     'SELECT * FROM product',
# ).scalar()
    # Product.objects.raw('SELECT * FROM product'):
    # Product.objects.filter(id=5).last()
    # Product.objects.get(id=5)


    products = Product.objects.all()
    # print(type(products))
    context = {'products': products}
    return render(request=request, template_name='products.html', context=context)
    # return HttpResponse("<p>Index page!</p>")

@csrf_exempt
def product_update(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    message = ""
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_quantity = request.POST.get('product_quantity')
        product_price = request.POST.get('product_price')
        product_active = request.POST.get('product_active')
        product_image = request.FILES.get('image')
        print("############", product_name)
        product_obj = Product.objects.filter(id=product_id).first()
        product_obj.product_name = product_name
        product_obj.product_description = product_description
        product_obj.product_quantity = product_quantity
        product_obj.product_price = product_price
        product_obj.product_image = product_image
        if product_active:
            product_obj.product_active = product_active
        else:
            product_obj.product_active = False
        product_obj.save()
        message = "Successfully updated product"
    context = {"product": product, "message": message}
    return render(request, 'product_update.html', context)

@login_required
def create_product(request):
    message = ""
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_quantity = request.POST.get('product_quantity')
        product_price = request.POST.get('product_price')
        # product_image = request.FILES['product_image']
        product_image = request.FILES.get('image')
        product_active = request.POST.get('product_active')

        Product.objects.create(product_name=product_name,
                            product_description=product_description,
                            product_quantity=product_quantity,
                            product_price=product_price,
                            product_image=product_image)
        message = "Successfully created"
    context = {"message": message}
    return render(request, 'product_create.html', context=context)

def product_delete(request, product_id):
    Product.objects.filter(id=product_id).delete()
    return JsonResponse({'message': f'successfully deleted {product_id}'}, safe=False)

@csrf_exempt
def user_login(request):
    message = ''
    if request.method == "POST":
        next_url = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('passwordtext')

        user = User.objects.filter(username=username).first()
        if not user:
            message = "User doesnt exist"
        
        if user:
            is_user = authenticate(request, username=username, password=password)
            if is_user:
                login(request, user)
                return redirect(next_url)
            else:
                message = "password is incorrect"
    context = {'message': message}
    return render(request, 'login.html', context)

@csrf_exempt
def registration(request):
    message = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('passwordtext')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        profile_image = request.POST.get('profile_image')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')

        line1 = request.POST.get('line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        address = Address.objects.create(line1=line1, city=city, state=state, country=country, zip_code=zip_code)
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, full_name= full_name, profile_image= profile_image, contact_number=contact_number, address=address, date_of_birth=date_of_birth)
        if user:
            message = 'Successfully created user'
            return redirect('/')
        else:
            message = 'Something went wrong'
    context= {'message': message}
    return render(request, 'registration.html', context)

def user_logout(request):
    logout(request)
    return redirect("/")

@csrf_exempt
def add_to_cart(request):
    try:
        if request.method == "POST":
            data = request.body.decode('utf-8')
            data = json.loads(data)
            quantity = data.get('quantity')
            product_id = data.get('product')
            product = get_object_or_404(Product, id=product_id)
            user_id = data.get('user')
            user = get_object_or_404(User, id=user_id)
            
            cart_product = CartDetail.objects.filter(product=product)
            if cart_product:
                quantity = int(quantity) + int(cart_product.quantity)
                CartDetail.objects.update(quantity=quantity)
            else:
                CartDetail.objects.create(product=product, user=user, quantity=quantity)
            return JsonResponse({'message': 'Successfully Added in cart'}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'message': f"Failed {e}"},safe=False, status=500)
    
def cart_detail(request):
    user_id = request.user.id
    products = CartDetail.objects.filter(user=user_id)
    context = {"products": products}
    return render(request, 'cart.html', context)

# @login_required
# class CartDetailView(View):
#     def get(self, request):
#         user_id = request.user.id
#         products = CartDetail.objects.filter(user=user_id)
#         context = {"products": products}
#         return render(request, 'cart.html', context)

#     def post(self, request):
#         # Handle POST request to add product to cart
#         # ...
#         return redirect('cart_detail')

#     def delete(self, request):
#         # Handle DELETE request to remove product from cart
#         # ...
#         return redirect('cart_detail')
    
def place_order(request):
    user_id = request.user.id
    products = CartDetail.objects.filter(user=user_id)
    order_number = int(time.time())
    for p in products:
        product = p.product
        user = p.user
        quantity = p.quantity
        total_price = 0
        order_status = "order place"
        OrderDetail.objects.create(product=product, user=user, quantity=quantity, total_price=total_price, order_status=order_status, order_number=order_number)
        CartDetail.objects.filter(product=product).delete()
    return JsonResponse({'message': 'Successfully Placed the order.'})

def order_details(request):
    user_id = request.user.id
    order_details = OrderDetail.objects.filter(user=user_id)
    orders_dict = {}
    for order in order_details:
        if order.order_number in orders_dict:
            orders_dict[order.order_number]['products'].append({'name': order.product.product_name,
                                                                 'quantity': order.quantity,
                                                                 'price': order.total_price,
                                                                 'status': order.order_status})
        else:
            orders_dict[order.order_number] = {'order_number': order.order_number,
                                                'products': [{'name': order.product.product_name,
                                                              'quantity': order.quantity,
                                                              'price': order.total_price,
                                                              'status': order.order_status}]}
    orders_list = list(orders_dict.values())
    context = {"orders": orders_list}
    # # return TemplateResponse(request, 'order_details.html', context)
    return render(request, 'order_details.html', context)
