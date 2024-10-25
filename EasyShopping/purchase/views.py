from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from core.models import Order

@login_required(login_url='login')
def payment(request):
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
        paymentMethod = request.POST.get('paymentMethod')
        orderAmount = int(request.POST.get('shippingFee')) + int(request.POST.get('orderAmount'))
        orders = Order.objects.filter(user=request.user, orderStatus='Processing')

        for order in orders:
            orderAmount = orderAmount
            order.paymentMethod = paymentMethod
            order.paymentDate = timezone.now()
            order.orderStatus = 'Completed'
            order.save()
        
        # Xóa trạng thái thanh toán trong session sau khi hoàn tất
        request.session.pop('is_payment_in_progress', None)

        return redirect('history')
    
    context = {
        'orders': orders,
        'totalAmount': request.POST.get('totalAmount'),
    }
    return render(request, 'checkout.html', context)