from django.shortcuts import render
from django.views import View
from unicodedata import category

from .models import Category,Product

class Home(View):
    def get(self,request):
        categories=Category.objects.all()
        products=Product.objects.all()
        return render(request,'index.html', {
            'categories':categories,
            'products':products,
        })