from django.shortcuts import render
from django.template.context_processors import request
from django.views import View
from unicodedata import category

from .models import Category,Product

class Home(View):
    def get(self,request):
        categories=Category.objects.all()
        products=Product.objects.all().order_by('-id')[:4]
        return render(request,'index.html', {
            'categories':categories,
            'products':products,
        })



class ProductsView(View):
    def get(self, request):
        product=Product.objects.all()
        return render(request,'products.html',
                      {'products_view':product})


class Product_Detail(View):
    def get(self,request,id):
        product=Product.objects.get(id=id)
        return render(request,'product_detail.html',{'product_detail':product})


