from django.contrib import admin
from .models import Product, Address, Profile, CartDetail, OrderDetail

# Register your models here.
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(CartDetail)
admin.site.register(OrderDetail)
