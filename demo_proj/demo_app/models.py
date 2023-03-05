from django.db import models

# Create your models here.
class Product(models.Model):
    # product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_description = models.TextField()
    product_image = models.ImageField()
    product_quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name_plural = 'Products'
    
# class User

# class Address

# class ContactDetail