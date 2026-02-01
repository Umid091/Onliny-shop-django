from django.db import models

from django.contrib.auth.models import AbstractUser
from products.models import Product

class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    email=models.EmailField(unique=True)
    image=models.ImageField(upload_to="user_image/",null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)


    def __str__(self):
       return  self.username


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlists')




