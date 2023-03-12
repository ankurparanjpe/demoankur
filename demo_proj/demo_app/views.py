from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

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
        print("############", product_name)
        product_obj = Product.objects.filter(id=product_id).first()
        product_obj.product_name = product_name
        product_obj.product_description = product_description
        product_obj.product_quantity = product_quantity
        product_obj.product_price = product_price
        if product_active:
            product_obj.product_active = product_active
        product_obj.save()
        message = "Successfully updated"
    context = {"product": product, "message": message}
    return render(request, 'product_update.html', context)
    
def create_product(request):
    message = ""
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_quantity = request.POST.get('product_quantity')
        product_price = request.POST.get('product_price')
        product_image = request.FILES['product_image']
        # product_image = request.POST.get('product_image')
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
    