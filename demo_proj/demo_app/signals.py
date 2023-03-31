from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver
from demo_app.models import Product

@receiver(post_save, sender=Product)
def my_handler(sender, **kwargs):
    print("Signal received!")

@receiver(pre_delete, sender=Product)
def mymodel_pre_delete(sender, instance, **kwargs):
    # do something before MyModel instance is deleted
    print("Signal received!")

@receiver(post_delete, sender=Product)
def mymodel_post_delete(sender, instance, **kwargs):
    # do something after MyModel instance is deleted
    print("Signal received!")

@receiver(pre_save, sender=Product)
def mymodel_pre_save(sender, instance, **kwargs):
    # do something before MyModel instance is saved
    print("Signal received!")
