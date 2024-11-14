
from core.models import *
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# tính trung bình đánh giá
def getRating(reviews):
    rating = 0
    if len(reviews) == 0: return 0
    for review in reviews:
        rating += review.rating
    return round(rating/len(reviews), 1)

# tính tổng số đơn hàng đã bán được của 1 sản phẩm
def getTotalSale(orders):
    sum = 0
    for order in orders:
        sum += order.itemQuantity
    return sum

def productDetailView(request, pid):
    product = Product.objects.get(productID = pid)

    if request.user.is_authenticated:
        user = request.user
        category = product.category

        userInterest, created = UserInterest.objects.get_or_create(user=user, category=category)
        
        userInterest.numberOfView += 1
        userInterest.timestamp = timezone.now()
        userInterest.save()
    
    reviews = Review.objects.filter(product=product).order_by('-reviewDate')

    rating = getRating(reviews)
    
    context = {
        "product" : product,
        "review" : reviews,
        "rating": rating,
        "totalSale": getTotalSale(Order.objects.filter(item__product__productID = pid))
    }
    return render(request, 'productDetail.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    Thêm sản phẩm vào giỏ hàng của người dùng.
    """
    user = request.user
    productID = request.data.get('productID')
    quantity = request.data.get('quantity', 1)
    sizeID = request.data.get('size')

    # Kiểm tra dữ liệu đầu vào
    if not productID or not sizeID:
        return Response({"error": "Product ID and Size are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Lấy hoặc tạo giỏ hàng cho người dùng
    cart, _ = Cart.objects.get_or_create(user=user)

    try:
        # Tìm sản phẩm dựa trên productID và sizeID
        item = Item.objects.get(product__productID=productID, size__sizeID=sizeID)
    except Item.DoesNotExist:
        return Response({"error": "Item does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    # Tăng số lượng sản phẩm nếu đã tồn tại
    cart_item.quantity += int(quantity)
    cart_item.save()

    # Cập nhật tổng tiền trong giỏ hàng
    cart.totalAmount += item.product.getNewPrice() * int(quantity)
    cart.save()

    return Response(data="success", status=status.HTTP_200_OK)