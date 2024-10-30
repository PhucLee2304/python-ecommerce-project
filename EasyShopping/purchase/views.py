from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import json
from core.models import Order, CartItem

# @login_required(login_url='login')
# def payment(request):
#     # Xóa trạng thái thanh toán nếu yêu cầu là DELETE
#     if request.method == 'DELETE':
#         request.session.pop('is_payment_in_progress', None)
#         return HttpResponse(status=200)
    
#     if 'is_payment_in_progress' in request.session:
#         cancellation_time = timezone.now() - timezone.timedelta(minutes=1)
#         Order.objects.filter(
#             user=request.user, 
#             orderStatus='Processing', 
#             orderDate__lt=cancellation_time
#         ).update(orderStatus='Cancelled')
        
#         # Xóa trạng thái thanh toán trong session
#         request.session.pop('is_payment_in_progress', None)

    
#     request.session['is_payment_in_progress'] = True

#     if request.method == 'POST':
#         orders = Order.objects.filter(user=request.user, orderStatus='Processing')

#         if orders.exists():
#             for order in orders:
#                 order.orderAmount = int(request.POST.get('shippingFee')) + int(request.POST.get('orderAmount'))
#                 order.paymentMethod = request.POST.get('paymentMethod')
#                 order.paymentDate = timezone.now()
#                 order.orderStatus = 'Completed'
#                 order.save()

#                 item = order.item  # Giả sử bạn có thuộc tính 'item' trong Order
#                 item.stockQuantity -= order.itemQuantity  # Giảm số lượng tồn kho theo số lượng đã đặt
#                 item.save()

#                 cartItem = CartItem.objects.filter(user=request.user, item=item).first()
#                 if cartItem:
#                     cartItem.delete()
        
#             # Xóa trạng thái thanh toán trong session sau khi hoàn tất
#             request.session.pop('is_payment_in_progress', None)

#         return redirect('history')
    
#     orders = Order.objects.filter(user=request.user, orderStatus='Processing')
#     totalAmount = sum(order.orderAmount for order in orders)
    
#     context = {
#         'orders': orders,
#         'totalAmount': totalAmount,
#     }
#     return render(request, 'checkout.html', context)

# @login_required
# def cancel_payment_session(request):
#     # Xóa trạng thái thanh toán khỏi session
#     request.session.pop('is_payment_in_progress', None)
#     return HttpResponse(status=200)

@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        paymentMethod = request.POST.get('paymentMethod')
        shippingFee = int(request.POST.get('shippingFee'))
        orderAmount = int(request.POST.get('orderAmount'))
        orderIDs = request.POST.getlist('orderID')

        for orderID in orderIDs:
            try:
                order = Order.objects.get(orderID=orderID)  
                order.orderAmount = orderAmount + shippingFee
                order.orderStatus = 'Completed'  
                order.paymentMethod = paymentMethod
                order.paymentDate = timezone.now()
                order.save()

                item = order.item  
                item.stockQuantity -= order.itemQuantity 
                item.save()

            except Order.DoesNotExist:
                pass

        return redirect('showOrder')

    elif request.method == 'DELETE':
        # Xử lý hủy đơn hàng
        data = json.loads(request.body)  # Lấy dữ liệu JSON từ body
        orderIDs = data.get('orderIDs', [])  # Lấy danh sách orderIDs từ dữ liệu
        for orderID in orderIDs:
            try:
                order = Order.objects.get(orderID=orderID)  
                order.orderStatus = 'Cancelled'  
                order.save()  # Lưu lại trạng thái đã hủy
            except Order.DoesNotExist:
                pass

        return JsonResponse({'success': True})
    
    else:
        user = request.user  
        orders = Order.objects.filter(user=user, orderStatus='Processing')  

        totalAmount = sum(order.orderAmount + order.item.product.shippingFee for order in orders)  

        context = {
            'user': user,
            'orders': orders,
            'totalAmount': totalAmount,
        }
        return render(request, 'checkout.html', context)
