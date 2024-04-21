from django.shortcuts import render
from accounts.models import Account
from products.models import Product
# Create your views here.

def home(request):
    account = Account.objects.all()
    return render(request, 'store/index.html', {'accounts': account})

def shop(request,id):
    account = Account.objects.get(id=id)
    products = Product.objects.filter(account=account)
    return render(request, 'store/shop.html', {'products': products,'account': account})

