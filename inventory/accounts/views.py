from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.
def login_page(request):
    return render(request, 'accounts/login.html')


def login(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            messages.success(request, 'Login successful')
            return render(request, 'home/dashboard.html')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login-page')