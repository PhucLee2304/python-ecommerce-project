from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import json
from core.models import Order

@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        paymentMethod = request.POST.get('paymentMethod')
        shippingFee = int(request.POST.get('shippingFee', 0))
        totalAmount = int(request.session.get('totalAmount', 0))
        orderIDs = [order['orderID'] for order in request.session.get('orders', [])]

        for orderID in orderIDs:
            try:
                order = Order.objects.get(orderID=orderID)  
                order.orderAmount += shippingFee
                order.orderStatus = 'Completed'  
                order.paymentMethod = paymentMethod
                order.paymentDate = timezone.now()
                order.save()

                item = order.item  
                item.stockQuantity -= order.itemQuantity 
                item.save()

            except Order.DoesNotExist:
                messages.warning(request, f"Order {orderID} does not exist.")
                continue
        
        del request.session['orders']
        del request.session['totalAmount']

        return redirect('showOrder')

    elif request.method == 'DELETE':
        # Cancel order
        data = json.loads(request.body)  # Get JSON data from body
        orderIDs = data.get('orderIDs', [])  # Get orderIDs list from data
        for orderID in orderIDs:
            try:
                order = Order.objects.get(orderID=orderID)  
                order.orderStatus = 'Cancelled'  
                order.save() 
            except Order.DoesNotExist:
                pass

        return JsonResponse({'success': True})
    
    else:
        user = request.user  
        orders = request.session.get('orders', [])  
        totalAmount = float(request.session.get('totalAmount'))

        context = {
            'user': user,
            'orders': orders,
            'totalAmount': float(totalAmount),
        }
        return render(request, 'checkout.html', context)
