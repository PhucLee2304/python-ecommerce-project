from django.shortcuts import render, get_object_or_404, redirect
from core.models import Order, Review

def history(request):
    user = request.user 
    orders = Order.objects.filter(user=user).order_by('-orderDate')

    for order in orders:
        if order.orderStatus == 'Delivered':
            order.orderStatus = 'Completed'
            order.save()

    if request.method == 'POST':
        orderID = request.POST.get('orderID')
        order = get_object_or_404(Order, orderID=orderID)
        if order.orderStatus == 'Pending':
            order.orderStatus = 'Cancelled'
            order.save()
        return redirect('history') 

    return render(request, 'history.html', {'orders': orders})