from django.http import JsonResponse
from django.shortcuts import render
from .models import OrderData
from products.models import Product
from django.db.models import Sum,Count
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond,
    )
# Create your views here.

def dashboard(request):
    print(request.user)
    total_products = Product.objects.filter(account__user=request.user).count()
    orders = OrderData.objects.filter(account__user=request.user)
    products = Product.objects.filter(account__user=request.user)
    low_stock = products.filter(stock__lte=10)
    daily_sale = OrderData.objects.filter(account__user = request.user).annotate(date=TruncDay('created_at')).values('date').annotate(total=Sum('order_total')).order_by('date')
    print(daily_sale)
    revenue = 0
    cp = 0
    for order in orders:
        revenue += order.order_total
        cp += order.order_cost
    if cp == 0:
        profit = 0
    else:
        profit = round(((revenue - cp)/cp)*100)
    total_orders = orders.count()
    return render(request, 'home/dashboard.html',{'total_products': total_products, 'total_orders': total_orders, 'revenue': revenue,'profit': profit, 'orders': orders,'low_stock': low_stock})


def charts_data(request):
    daily_sale = OrderData.objects.filter(account__user = request.user).annotate(date=TruncDay('created_at')).values('date').annotate(total=Sum('order_total')).order_by('date')
    daily_orders_count = OrderData.objects.filter(account__user = request.user).annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
    dataX2 = []
    dataY2 = []
    for sale in daily_orders_count:
        dataX2.append(sale['date'].strftime('%Y-%m-%d'))
        dataY2.append(sale['count'])
    dataX = []
    dataY = []
    for sale in daily_sale:
        dataX.append(sale['date'].strftime('%Y-%m-%d'))
        dataY.append(sale['total'])
    daily_sale = {
        'dataX': dataX,
        'dataY': dataY,
        'dataX2': dataX2,
        'dataY2': dataY2

    }
    return JsonResponse(daily_sale)