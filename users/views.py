

import random
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login
from .models import User, EmailVerify


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': "Bu username band!"})

        if password != password_confirm:
            return render(request, 'auth/register.html', {'error': "Parollar mos kelmadi!"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        generated_code = str(random.randint(100000, 999999))

        EmailVerify.objects.update_or_create(
            email=email,
            defaults={'code': generated_code, 'is_confirmed': False}
        )

        try:
            send_mail(
                subject="Luxury Watches - Tasdiqlash kodi",
                message=f"Sizning tasdiqlash kodingiz hechkimga bermang hattoki UMID ga ham: {generated_code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            user.delete()
            return render(request, 'auth/register.html', {'error': "Email yuborishda xatolik yuz berdi."})


        request.session['temp_user_email'] = email
        return redirect('email_verify')


class VerifyEmailView(View):
    def get(self, request):
        return render(request, 'auth/email_verify.html')

    def post(self, request):
        code_input = request.POST.get('code', '').strip()
        email_session = request.session.get('temp_user_email')

        if not email_session:
            return redirect('register')

        otp = EmailVerify.objects.filter(email=email_session, code=code_input, is_confirmed=False).last()

        if otp:
            if timezone.now() <= otp.expiration_time:
                user = User.objects.get(email=email_session)
                user.is_active = True
                user.save()

                otp.is_confirmed = True
                otp.save()

                del request.session['temp_user_email']
                messages.success(request, "Email muvaffaqiyatli tasdiqlandi!")
                return redirect('login')
            else:
                return render(request, 'auth/verfy_email.html', {'error': "Kodning amal qilish muddati tugagan!"})

        return render(request, 'auth/verfy_email.html', {'error': "Tasdiqlash kodi xato kiritildi!"})


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {username}!")
                return redirect('index')
            else:
                return render(request, 'auth/login.html',
                              {'error': "Profilingiz faollashtirilmagan. Emailingizni tekshiring."})
        else:
            return render(request, 'auth/login.html', {'error': "Username yoki parol xato."})


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


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Product, Wishlist


class WishlistToggleView(View):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)

            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )

            if not created:
                wishlist_item.delete()
                messages.info(request, "Mahsulot tanlanganlardan olib tashlandi.")
            else:
                messages.success(request, "Mahsulot tanlanganlarga qo'shildi.")

            return redirect(request.META.get('HTTP_REFERER', 'index'))

        else:
            messages.info(request, "Tanlanganlarga qo'shish uchun avval tizimga kiring!")
            return redirect('login')


class WishlistListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            items = Wishlist.objects.filter(user=request.user)
            return render(request, 'wishlist.html', {'wishlist_items': items})
        else:
            messages.info(request, "Tanlanganlar ro'yxatini ko'rish uchun tizimga kiring!")
            return redirect('login')