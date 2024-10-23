from django.shortcuts import render, redirect
from .models import Order

def show(request):
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    # if not request.user.is_authenticated:
    #     # Nếu chưa đăng nhập, chuyển hướng người dùng đến trang đăng nhập
    #     return redirect('login')  # Thay 'login' bằng tên URL của trang đăng nhập của bạn

    # Nếu đã đăng nhập, tiếp tục lấy đơn hàng
    # Lấy khách hàng từ đối tượng người dùng đã đăng nhập
    customer = request.user.customer  # Giả định rằng bạn có một quan hệ một-một từ User đến Customer
    # Lấy tất cả các đơn hàng của khách hàng, sắp xếp theo ngày đặt hàng mới nhất
    orders = Order.objects.all().filter(customer=customer).order_by('-orderDate')  # Sắp xếp theo ngày mới nhất
    # except AttributeError:
    #     # Nếu không tìm thấy customer, trả về danh sách rỗng
    #     orders = []
    
    # Truyền danh sách đơn hàng vào context để hiển thị trong template
    for order in orders:
        print(f"Order ID: {order.orderID}, Customer: {order.customer}, "
              f"Item: {order.item}, Date: {order.orderDate}, "
              f"Quantity: {order.itemQuantity}, Status: {order.orderStatus}")

    return render(request, 'history.html', {'orders': orders})

