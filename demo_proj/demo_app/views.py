from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.
def index(request):
#     num_users = User.objects.raw(
#     # select * from Product
#     'SELECT * FROM product',
# ).scalar()
    # Product.objects.raw('SELECT * FROM product'):
    Product.objects.filter(id=5).last()
    # Product.objects.get(id=5)


    products = Product.objects.all()
    # print(type(products))
    context = {'products': products}
    return render(request=request, template_name='products.html', context=context)
    # return HttpResponse("<p>Index page!</p>")


def product_update(request, product_id):
    print("@@@@@@@@@@@@@@@@@@@@", product_id)
    return HttpResponse("<p>Product description page!</p>")
    