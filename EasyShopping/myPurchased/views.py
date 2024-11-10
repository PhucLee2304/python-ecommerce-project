from django.shortcuts import get_object_or_404, redirect, render
from core.models import Order

def myPurchasedView(request, detail):
    
    user = request.user 
    if detail == 'All':
        orders = Order.objects.filter(user=user).order_by('-orderDate')
        context = {
            'orders' : orders,
            'message' : detail
            
        }
        
        return render(request, 'myPurchased.html', context)
    else:
        orders = Order.objects.filter(user=user, orderStatus=detail).order_by('-orderDate')
        context = {
            'orders' : orders,
            'message' : detail
            
        }
        
        return render(request, 'myPurchased.html', context)
        

    # for order in orders:
    #     if order.orderStatus == 'Delivered':
    #         order.orderStatus = 'Completed'
    #         order.save()

    # if request.method == 'POST':
    #     orderID = request.POST.get('orderID')
    #     order = get_object_or_404(Order, orderID=orderID)
    #     if order.orderStatus == 'Pending':
    #         order.orderStatus = 'Cancelled'
    #         order.save()
    #     return redirect('history') 

    
    

def cancelView(request, oid):
    order = Order.objects.get(orderID = oid)
    order.delete()
    return redirect('my-purchased', detail = 'All') 
    
