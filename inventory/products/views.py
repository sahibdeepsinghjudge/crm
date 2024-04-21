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
    total_product_value = 0
    for product in products:
        total_product_value += product.selling_price * product.stock
    return render(request, 'products/products.html', {'products': products, 'total_product_value': total_product_value})

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


def search_products_catalog(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        products = Product.objects.filter(name__icontains=search)
        return render(request, 'products/catalog.html', {'products': products})

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
    return redirect('catalog')

def product_catalog(request):
    products = Product.objects.filter(account__user=request.user)
    return render(request, 'products/catalog.html', {'products': products})

def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    if product.stock == 0:
        messages.info(request, 'Product out of stock')
        return redirect('catalog')
    order = OrderData.objects.get(order_id=request.session['order'])
    products = order.products
    products = products + ',' + str(product.id)
    order.products = products
    order.save()
    messages.success(request, 'Product added to cart')
    return redirect('catalog')

def remove_from_cart(request, index):
    order = OrderData.objects.get(order_id=request.session['order'])
    products = order.products
    products = products.split(',')
    del products[index]
    products = ','.join(products)
    order.products = products
    order.save()
    messages.success(request, 'Product removed from cart')
    return redirect('billing')

'''
    {
        'prod_id': 1,
        'qty': 2
    }
'''
def billing_cart(request):
    order = OrderData.objects.get(order_id=request.session['order'])
    products = order.products.split(',')
    products = products[1:]
    return_products = []
    for i in products:
        return_products.append(Product.objects.get(id=i))
    total = 0
    total_tax = 0
    order_cost = 0
    for product in return_products:
        total += product.selling_price
        total_tax +=  product.selling_price * (product.gst)/100 
        order_cost += product.cost_price
    order.order_total = total
    order.order_tax = total_tax
    order.order_cost = order_cost
    order.save()
    total_tax = round(total_tax, 2)
    return render(request, 'home/billing.html', {'products': return_products, 'order': order,'total': total+total_tax, 'total_tax': total_tax})


def complete_order(request):
    order = OrderData.objects.get(order_id=request.session['order'])
    products = order.products.split(',')
    products = products[1:]
    for i in products:
        prod = Product.objects.get(id=i)
        prod.stock -= 1
        prod.save()
    order.is_paid = True
    request.session['order'] = None
    order.save()
    messages.success(request, 'Order completed successfully')
    return redirect('view-products')


def bill(request,id):
    try:
        order  = OrderData.objects.get(id=id)
        products = order.products.split(',')
        products = products[1:]
        return_products = []
        for i in products:
            return_products.append(Product.objects.get(id=i))
        return render(request,'home/bill.html',{'products':return_products,'order':order})
    except Exception as e:
        print(e)
        pass
    
        

