from django.shortcuts import render, redirect
from core.models import Cart, CartItem
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
            'priceAfterDiscount': round(product.getNewPrice()),
            'discount': product.discount,
            'quantity': cartItem.quantity,
            'totalPrice': cartItem.quantity * round(product.getNewPrice()),
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

def processPurchase(request, cart):
    selectedItems = request.POST.getlist('selectProduct[]')

    if not selectedItems:
        messages.info(request, 'No products selected for purchase')
        return redirect('cartShow') 

    items = [] 
    for i, itemID in enumerate(selectedItems, 1):
        quantity = request.POST.get(f'quantity{i}')
        if quantity:
            items.append({
                'itemID': itemID,
                'quantity': int(quantity),
            })

    if items:
        context = {
            'items': items,
        }
        return render(request, 'purchase.html', context)

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
            return processPurchase(request, cart)
 
    return redirect('cartShow')

@login_required(login_url='login')
def purchase(request):
    return render(request, 'purchase.html')