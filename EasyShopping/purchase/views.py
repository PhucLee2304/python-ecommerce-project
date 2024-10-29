from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from core.models import Order

@login_required(login_url='login')
def payment(request):
    # Xóa trạng thái thanh toán nếu yêu cầu là DELETE
    if request.method == 'DELETE':
        request.session.pop('is_payment_in_progress', None)
        return HttpResponse(status=200)
    
    if 'is_payment_in_progress' in request.session:
        cancellation_time = timezone.now() - timezone.timedelta(minutes=1)
        Order.objects.filter(
            user=request.user, 
            orderStatus='Processing', 
            orderDate__lt=cancellation_time
        ).update(orderStatus='Cancelled')
        
        # Xóa trạng thái thanh toán trong session
        request.session.pop('is_payment_in_progress', None)

    
    request.session['is_payment_in_progress'] = True

    if request.method == 'POST':
        orders = Order.objects.filter(user=request.user, orderStatus='Processing')

        for order in orders:
            order.orderAmount = int(request.POST.get('shippingFee')) + int(request.POST.get('orderAmount'))
            order.paymentMethod = request.POST.get('paymentMethod')
            order.paymentDate = timezone.now()
            order.orderStatus = 'Completed'
            order.save()
        
        # Xóa trạng thái thanh toán trong session sau khi hoàn tất
        request.session.pop('is_payment_in_progress', None)

        return redirect('history')
    
    orders = Order.objects.filter(user=request.user, orderStatus='Processing')
    totalAmount = sum(order.orderAmount for order in orders)
    
    context = {
        'orders': orders,
        'totalAmount': totalAmount,
    }
    return render(request, 'checkout.html', context)

@login_required
def cancel_payment_session(request):
    # Xóa trạng thái thanh toán khỏi session
    request.session.pop('is_payment_in_progress', None)
    return HttpResponse(status=200)