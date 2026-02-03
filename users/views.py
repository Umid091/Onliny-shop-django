from http.cookiejar import request_path

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, logout,login
from django.contrib import messages
from .models import User


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')

        if password != confirm_password:
            messages.error(request, "Parollar mos kelmadi!")
            return render(request, 'auth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi band!")
            return render(request, 'auth/register.html')

        user = User.objects.create_user(
            username=username,
            phone=phone,
            password=password,
            age=age,
            email=email,
            image=image,
        )

        login(request, user)
        messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect('login')



class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Username yoki parol xato!")
            return render(request, 'auth/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')



class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'auth/profile.html', {'user_data': request.user})
        else:

            messages.info(request, "Profilni ko'rish uchun avval ro'yxatdan o'ting!")
            return redirect('register')