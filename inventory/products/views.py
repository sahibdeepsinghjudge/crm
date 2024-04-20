from django.shortcuts import redirect, render

from accounts.models import Account
from .models import Category, Product
from django.contrib import messages
from home.models import OrderData

def add_products(request):
    return render(request, 'products/add_products.html')

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('description')
        product_category = request.POST.get('category')
        product_image = request.POST.get('image')
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')
        stock = request.POST.get('stock')
        gst = request.POST.get('gst')
        units = request.POST.get('unit')
        product_image = request.FILES.get('image')
        try:
            category = Category.objects.get(name=product_category)
            account = Account.objects.get(user=request.user)
            Product.objects.create(name=product_name, description=product_description, category=category, image=product_image, cost_price=cost_price, selling_price=selling_price, stock=stock, gst=gst, units=units, account=account)
            messages.success(request, 'Product added successfully')
            return redirect('add-products')
        except Exception as e:
            print(e)
            messages.info(request, 'Account not found')
            redirect("login-page")
        return redirect('add-products')
    
def view_products(request):
    products = Product.objects.filter(account__user=request.user)
    return render(request, 'products/products.html', {'products': products})

def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('description')
        product_category = request.POST.get('category')
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')
        stock = request.POST.get('stock')
        gst = request.POST.get('gst')
        units = request.POST.get('unit')
        try:
            category = Category.objects.get(name=product_category)
            product.name = product_name
            product.description = product_description
            product.category = category
            product.cost_price = cost_price
            product.selling_price = selling_price
            product.stock = stock
            product.gst = gst
            product.units = units
            product.save()
            messages.success(request, 'Product updated successfully')
            return redirect('view-products')
        except Exception as e:
            print(e)
            messages.info(request, 'Account not found')
            redirect("login-page")
        return redirect('view-products')
    return render(request, 'products/edit_products.html', {'product': product})

def search_products(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        products = Product.objects.filter(name__icontains=search)
        return render(request, 'products/products.html', {'products': products})
    return redirect('view-products')


def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('view-products')


def initiate_order(request):
    account = Account.objects.get(user=request.user)
    order = OrderData.objects.create(account=account)
    request.session['order'] = order.order_id
    messages.success(request, 'Order initiated successfully')
    return redirect('view-products')