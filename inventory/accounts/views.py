from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Account
# Create your views here.
def login_page(request):
    return render(request, 'accounts/login.html')


def login(request):
    if request.method== 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=email).username
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.success(request, 'Login successful')
                return redirect('dashboard')
            else:
                messages.info(request, 'Invalid username or password')
                return redirect('login-page')
        except:
            messages.info(request, 'Invalid username or password')
            return redirect('login-page')
        

def register_page(request):
    return render(request, 'accounts/register.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        for i in username:
            if i == ' ':
                messages.info(request, 'Username cannot contain spaces')
                return redirect('register-page')
            
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gst = request.POST.get('gst')
        fssai = request.POST.get('fssai')
        User.objects.create_user(username=username, email=email, password=password)
        try:
            user = User.objects.get(email=email)
            Account.objects.create(phone=phone_number, address=address, gst=gst, fssai=fssai, user=user)
            messages.success(request, 'Account created successfully')
            return redirect('login-page')
        except:
            messages.info(request, 'Account creation failed')
            return redirect('register-page')
       