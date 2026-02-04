from django.urls import path

from .models import EmailVerify
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email_verify',VerifyEmailView.as_view(),name='email_verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(),name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist_page'),
    path('wishlist/toggle/<int:product_id>/', WishlistToggleView.as_view(), name='toggle_wishlist'),


]