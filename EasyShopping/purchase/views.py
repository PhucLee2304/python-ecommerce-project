from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
import json
import qrcode
# from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import base64
from io import BytesIO
from core.models import *

# @login_required(login_url='login')
# def cashOnDelivery(request):
#     if request.method == 'POST':
#         paymentMethod = request.POST.get('paymentMethod')
#         shippingFee = int(request.POST.get('shippingFee', 0))
#         totalAmount = int(request.session.get('totalAmount', 0))
#         orderIDs = [order['orderID'] for order in request.session.get('orders', [])]

#         for orderID in orderIDs:
#             try:
#                 order = Order.objects.get(orderID=orderID)  
#                 order.orderAmount += shippingFee
#                 order.orderStatus = 'Completed'  
#                 order.paymentMethod = paymentMethod
#                 order.paymentDate = timezone.now()
#                 order.save()

#                 item = order.item  
#                 item.stockQuantity -= order.itemQuantity 
#                 item.save()

#             except Order.DoesNotExist:
#                 messages.warning(request, f"Order {orderID} does not exist.")
#                 continue
        
#         del request.session['orders']
#         del request.session['totalAmount']

#         return redirect('history')

#     elif request.method == 'DELETE':
#         # Cancel order
#         data = json.loads(request.body)  # Get JSON data from body
#         orderIDs = data.get('orderIDs', [])  # Get orderIDs list from data
#         for orderID in orderIDs:
#             try:
#                 order = Order.objects.get(orderID=orderID)  
#                 order.orderStatus = 'Cancelled'  
#                 order.save() 
#             except Order.DoesNotExist:
#                 pass

#         return JsonResponse({'success': True})
    
#     else:
#         user = request.user  
#         orders = request.session.get('orders', [])  
#         totalAmount = float(request.session.get('totalAmount'))

#         context = {
#             'user': user,
#             'orders': orders,
#             'totalAmount': float(totalAmount),
#         }
#         return render(request, 'checkout.html', context)

# @login_required(login_url='login')
# def bankTransfer(request):
#     if request.method == 'POST':
#         paymentMethod = request.POST.get('paymentMethod')
#         shippingFee = int(request.POST.get('shippingFee', 0))
#         totalAmount = int(request.session.get('totalAmount', 0))
#         orderIDs = [order['orderID'] for order in request.session.get('orders', [])]

#         qrData = ';'.join(map(str, orderIDs)) 
#         request.session['qrData'] = qrData

#         for orderID in orderIDs:
#             try:
#                 order = Order.objects.get(orderID=orderID)  
#                 order.orderAmount += shippingFee
#                 order.orderStatus = 'Pending'  
#                 order.paymentMethod = paymentMethod
#                 order.save() 

#             except Order.DoesNotExist:
#                 messages.warning(request, f"Order {orderID} does not exist.")
#                 continue

#         qrImage = qrcode.make(qrData)
#         buffered = BytesIO()
#         qrImage.save(buffered, format="PNG")
#         qr_base64 = base64.b64encode(buffered.getvalue()).decode()

#         return render(request, 'qr.html', {'qr_base64': qr_base64, 'totalAmount': totalAmount})
    
#     else:
#         user = request.user  
#         orders = request.session.get('orders', [])  
#         totalAmount = float(request.session.get('totalAmount'))

#         context = {
#             'user': user,
#             'orders': orders,
#             'totalAmount': float(totalAmount),
#         }
#         return render(request, 'checkout.html', context)

@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        print("Received POST request")
        paymentMethod = request.POST.get('paymentMethod')
        shippingFee = int(request.POST.get('shippingFee', 0))
        totalAmount = int(request.session.get('totalAmount', 0))
        orderIDs = [order['orderID'] for order in request.session.get('orders', [])]

        print(f"Payment Method: {paymentMethod}")
        print(f"Order IDs: {orderIDs}")
        
        if not paymentMethod:
            messages.error(request, 'Select a payment method')
            return redirect('payment')
        
        if paymentMethod == 'Cash On Delivery':
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

            return redirect('history')
    
        elif paymentMethod == 'Bank Transfer':
            qrData = ';'.join(map(str, orderIDs)) 
            request.session['qrData'] = qrData

            for orderID in orderIDs:
                try:
                    order = Order.objects.get(orderID=orderID)  
                    order.orderAmount += shippingFee
                    order.orderStatus = 'Pending'  
                    order.paymentMethod = paymentMethod
                    order.save() 

                except Order.DoesNotExist:
                    messages.warning(request, f"Order {orderID} does not exist.")
                    continue

            qrImage = qrcode.make(qrData)
            buffered = BytesIO()
            qrImage.save(buffered, format="PNG")
            qr_base64 = base64.b64encode(buffered.getvalue()).decode()

            return render(request, 'qr.html', {'qr_base64': qr_base64, 'totalAmount': totalAmount})

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
    
@csrf_exempt
def scan(request):
    if request.method == 'POST':
        qrInput = request.POST.get('qrInput')
        
        if not qrInput:
            return redirect('scan')
        
        if qrInput == request.session.get('qrData', ''):
            qrCodeList = qrInput.split(';')
            for qrCode in qrCodeList:
                try:
                    order = Order.objects.get(orderID=int(qrCode))
                    order.orderStatus = 'Shipping'  
                    order.paymentDate = timezone.now()
                    order.save()

                    item = order.item  
                    item.stockQuantity -= order.itemQuantity 
                    item.save()

                except Order.DoesNotExist:
                    messages.info(request, 'Order {qrCode} does not exist')
                    return redirect('payment')
                
            return redirect('history')
        else:
            messages.info(request, 'Wrong code. Scan again to get correct code')
            qrData = request.session.get('qrData', '')
            qrImage = qrcode.make(qrData)
            buffered = BytesIO()
            qrImage.save(buffered, format="PNG")
            qr_base64 = base64.b64encode(buffered.getvalue()).decode()
            return render(request, 'qr.html', {'qr_base64': qr_base64})
            
    else:
        return render(request, 'qr.html')
            

# views.py
from django.shortcuts import render

def checkoutView(request):
    product_id = request.GET.get('pid')  # Get product ID from the query parameter
    size_id = request.GET.get('sid')  # Get size ID from the query parameter
    quantity = request.GET.get('quantity')  # Get quantity from the query parameter
    product = Product.objects.get(productID = product_id)
    total = int(quantity) * float(product.price)
    context = {
        "product" : product,
        "total" : total,
        "quantity": quantity
    }

    # Process the data (e.g., retrieve product, size, and validate quantity)
    # Your logic to handle the checkout goes here

    return render(request, 'checkout.html', context)
