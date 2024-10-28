from django.shortcuts import render, redirect
from core.models import Cart, CartItem, Item, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def cartShow(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = []
    totalAmount = 0

    if cart:
        cartItems = CartItem.objects.filter(cart=cart)
        if not cartItems.exists():
            messages.info(request, "Your cart is empty")
    else:
        messages.info(request, "Your cart is empty")
        cartItems = []

    for cartItem in cartItems:
        product = cartItem.item.product
        size = cartItem.item.size
        item = {
            'itemID': cartItem.item.itemID,
            'productName': product.productName,
            'productImage': product.productImage.url,
            'sizeName': size.sizeName,
            'price': product.price,
            'priceAfterDiscount': product.getNewPrice(),
            'discount': product.discount,
            'quantity': cartItem.quantity,
            'totalPrice': cartItem.quantity * product.getNewPrice(),
        }
        items.append(item)
        totalAmount += item['totalPrice']

    context = { 
        'items': items,
        'totalAmount': totalAmount,
    }
    return render(request, 'cart.html', context)

def deleteProductFromCart(request, cart):
    itemID = request.POST.get('deleteProduct')

    try:
        cartItem = CartItem.objects.get(cart=cart, item__itemID=itemID)
        cartItem.delete()
        return redirect('cartShow')
    except CartItem.DoesNotExist:
        messages.info(request, "Item not found in cart")
    
    return redirect('cartShow')

def deleteAllFromCart(request, cart):
    CartItem.objects.filter(cart=cart).delete()
    return redirect('cartShow')

def getUserInformation(request):
    user = request.user
    full_name = user.full_name()
    address = user.address
    phone = user.phone

    if full_name == ' ' or not address or not phone:
        messages.info(request, 'Enter your information')
        return None
    
    return {
        'full_name': full_name,
        'address': address,
        'phone': phone,
    }

def addToPurchase(request, cart):
    user = getUserInformation(request)
    if user is None:
        return redirect('profile')
    
    selectedItems = request.POST.getlist('selectProduct[]')

    if not selectedItems:
        messages.info(request, 'No products selected for purchase')
        return redirect('cartShow') 

    orders = []
    outOfStockItems = []
    totalAmount = 0
    for i, itemID in enumerate(selectedItems, 1):
        quantity = request.POST.get(f'quantity{i}')
        if quantity:
            item = Item.objects.get(itemID=itemID)
            availableStock = item.stockQuantity

            if availableStock >= int(quantity):
                order = Order.objects.create(
                    user = user,
                    item = item,
                    orderAmount = int(quantity) * item.product.getNewPrice(),
                    itemQuantity = int(quantity),
                )
                orders.append(order)
                totalAmount += order.orderAmount + order.item.product.shippingFee
            else: 
                outOfStockItems.append(f'{item.product.productName} (Size: {item.size.sizeName})')

    if outOfStockItems:
        messages.info(request, f'The following items are out of stock: {'\n'.join(outOfStockItems)}')
        return redirect('cartShow')

    if orders:
        context = {
            'user': user,
            'orders': orders,
            'totalAmount': totalAmount,
        }
        return render(request, 'checkout.html', context)

    return redirect('cartShow')
    

@login_required(login_url='login')
def cartActions(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        messages.info(request, "Your cart is empty")
        return redirect('cartShow')

    if request.method == 'POST':
        if 'deleteProduct' in request.POST:
            return deleteProductFromCart(request, cart)
        
        elif 'deleteAll' in request.POST:
            return deleteAllFromCart(request, cart)
        
        elif 'buyAll' in request.POST:
            return addToPurchase(request, cart)
 
    return redirect('cartShow')