from django.db import models

from django.contrib.auth.models import AbstractUser
from products.models import Product

from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    email=models.EmailField(unique=True)
    image=models.ImageField(upload_to="user_image/",null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)


    def __str__(self):
       return  self.username


class EmailVerify(models.Model):
    email=models.EmailField(unique=True)
    code=models.CharField(max_length=6)
    is_confirmed=models.BooleanField(default=False)
    expiration_time=models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expiration_time = timezone.now() + timedelta(minutes=3)

        super(EmailVerify, self).save(*args, **kwargs)

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlists')




