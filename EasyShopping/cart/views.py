from django.shortcuts import render, redirect
from core.models import Cart, CartItem, Item, Order, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def deleteProductFromCart(request, cart, itemID):
    try:
        cartItem = CartItem.objects.get(cart=cart, item__itemID=itemID)
        cartItem.delete()
        return redirect('cart')
    except CartItem.DoesNotExist:
        messages.info(request, "Item not found in cart")
    
    return redirect('cart')

def deleteAllFromCart(request, cart):
    CartItem.objects.filter(cart=cart).delete()
    return redirect('cart')

def getUserInformation(request):
    user = request.user

    if user.is_authenticated:
        full_name = user.full_name()
        address = user.address
        phone = user.phone

        if not full_name or not address or not phone:
            messages.info(request, 'Enter your information')
            return None
        return user

    return None

def addToPurchase(request, cart):
    user = getUserInformation(request)
    if user is None:
        return redirect('profile')
    
    selectedItems = request.POST.getlist('selectProduct[]')

    if not selectedItems:
        messages.info(request, 'No products selected for purchase')
        return redirect('cart') 

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
        return redirect('cart')

    if orders:
        context = {
            'user': user,
            'orders': orders,
            'totalAmount': totalAmount,
        }
        return redirect('payment')

    return redirect('cart')

def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    totalAmount = 0
    cartItems = []

    if cart:
        cartItems = CartItem.objects.filter(cart=cart)
        if not cartItems.exists():
            messages.info(request, "Your cart is empty")
    else:
        messages.info(request, "Your cart is empty")

    for cartItem in cartItems:
        amountUnit = cartItem.quantity * cartItem.item.product.getNewPrice()
        totalAmount += amountUnit
        cartItem.amountUnit = amountUnit
    
    if request.method == 'POST':
        if 'deleteProduct' in request.POST:
            itemID = request.POST.get('deleteProduct')
            return deleteProductFromCart(request, cart, itemID)
        elif 'deleteAll' in request.POST:
            return deleteAllFromCart(request, cart)
        elif 'buyAll' in request.POST:
            return addToPurchase(request, cart)

    context = { 
        'cartItems': cartItems,
        'totalAmount': totalAmount,
    }
    return render(request, 'cart.html', context)