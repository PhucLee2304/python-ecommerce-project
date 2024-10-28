from django.shortcuts import render, redirect
from core.models import Order

def show(request):
    user = request.user  # Giả định rằng bạn có một quan hệ một-một từ User đến Customer
    orders = Order.objects.all().filter(user=user).order_by('-orderDate')  # Sắp xếp theo ngày mới nhất
    
    # Truyền danh sách đơn hàng vào context để hiển thị trong template
    # for order in orders:
    #     print(f"Order ID: {order.orderID}, Customer: {order.customer}, "
    #           f"Item: {order.item}, Date: {order.orderDate}, "
    #           f"Quantity: {order.itemQuantity}, Status: {order.orderStatus}")

    return render(request, 'history.html', {'orders': orders})

