
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('products/', views.ProductsView.as_view(),name='products')
]


