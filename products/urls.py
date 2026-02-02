
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('products/', views.ProductsView.as_view(),name='products'),
    path('product/<int:id>/', views.Product_Detail.as_view(), name='product_detail'),
]


