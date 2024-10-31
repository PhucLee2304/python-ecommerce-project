from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
import json
import qrcode
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import base64
from io import BytesIO
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

'''
def payment(request):
    if request.method == 'POST':
        paymentMethod = request.POST.get('paymentMethod')
        shippingFee = int(request.POST.get('shippingFee', 0))
        totalAmount = int(request.session.get('totalAmount', 0))
        orderIDs = [order['orderID'] for order in request.session.get('orders', [])]

        qrData = "" 

        for orderID in orderIDs:
            try:
                order = Order.objects.get(orderID=orderID)  
                order.orderAmount += shippingFee
                order.orderStatus = 'Pending'  
                order.paymentMethod = paymentMethod
                order.save()

                qrData += f"{order.orderID};"  

            except Order.DoesNotExist:
                messages.warning(request, f"Order {orderID} does not exist.")
                continue

        qrImage = qrcode.make(qrData.strip())
        
        # Lưu mã QR vào bộ nhớ
        buffered = BytesIO()
        qrImage.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Lưu thời gian tạo mã QR vào session
        request.session['qr_timestamp'] = timezone.now().timestamp()

        return render(request, 'qr.html', {'qr_base64': qr_base64, 'totalAmount': totalAmount})
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

@csrf_exempt
def scan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qrInput = data.get('qrInput')

            if not qrInput:
                return JsonResponse({'success': False, 'error': 'No QR code provided', 'redirect_url': reverse('qr')}, status=400)

            try:
                order = Order.objects.get(orderID=int(qrInput.strip()))
                order.orderStatus = 'Shipping'  
                order.paymentDate = timezone.now()
                order.save()

                item = order.item  
                item.stockQuantity -= order.itemQuantity 
                item.save()

                return JsonResponse({'success': True, 'redirect_url': reverse('showOrder')})
            except Order.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Order does not exist', 'redirect_url': reverse('qr')}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data', 'redirect_url': reverse('qr')}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
'''
