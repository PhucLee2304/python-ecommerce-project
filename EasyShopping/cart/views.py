import json
from django.shortcuts import get_object_or_404, render, redirect
from core.models import *
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
        messages.info(request, 'Complete your profile information')
        return redirect('profile')

    selectedItems = request.POST.getlist('selectProduct[]') 
    quantities = request.POST.getlist('quantity[]')  
    itemIDs = request.POST.getlist('itemID[]') 

    # print("Selected Items:", selectedItems)
    # print("Quantities:", quantities)
    # print("Item IDs:", itemIDs)

    if not selectedItems:
        messages.info(request, 'No products selected for purchase')
        return redirect('cart')

    orders = []
    outOfStockItems = []
    totalAmount = 0

    for index, itemID in enumerate(itemIDs):
        if itemID in selectedItems:
            try:
                quantity = int(quantities[index]) 
                if quantity <= 0:
                    messages.error(request, f"Quantity must be greater than zero for item {itemID}.")
                    continue

                item = Item.objects.get(itemID=itemID) 
                if item:
                    availableStock = item.stockQuantity
                    if availableStock >= quantity:
                        order = Order.objects.create(
                            user=user,
                            item=item,
                            orderAmount=quantity * item.product.getNewPrice(),
                            itemQuantity=quantity,
                        )
                        orders.append(order) 
                        totalAmount += order.orderAmount + float(order.item.product.shippingFee)
                    else:
                        outOfStockItems.append(f'{item.product.productName} (Size: {item.size.sizeName})')
                        continue
                else:
                    messages.warning(request, f"Item {itemID} does not exist.")

            except ValueError:
                messages.error(request, f"Invalid quantity for item {itemID}.")
                continue

    if outOfStockItems:
        messages.info(request, f'The following items are out of stock: {'\n'.join(outOfStockItems)}')
        return redirect('cart')

    if orders:
        print("Orders to be processed:", orders)  
        print("Total amount:", totalAmount)
        request.session['orders'] = [
            {
                'orderID': order.orderID,
                'itemID': order.item.itemID,
                'productImage': order.item.product.productImage.url,
                'productName': order.item.product.productName,
                'quantity': order.itemQuantity,
                'orderAmount': float(order.orderAmount),
                'discountPrice': float(order.item.product.getNewPrice()),
                'shippingFee': float(order.item.product.shippingFee),
            } for order in orders
        ]
        request.session['totalAmount'] = float(totalAmount)

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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_cart_item(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        cart_item = CartItem.objects.get(id=data['cartItemID'])
        cart_item.quantity = data['quantity']
        cart_item.save()
        newTotal = cart_item.quantity * cart_item.item.product.price
        return JsonResponse({'success': True, 'newTotal' : newTotal})

@csrf_exempt
def update_cart_item_size(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get the CartItem
        cart_item = get_object_or_404(CartItem, id=data['cartItemID'])
        
        # Get the new Size
        new_size = get_object_or_404(Size, sizeID=data['sizeID'])
        
        # print(new_size)
        
        items = Item.objects.filter(product = cart_item.item.product)
        
        for i in items:
            if i.size == new_size:
                newItem = i
        
        
        # Update the item's size
        cart_item.item = newItem
        
        # Save the updated item
        cart_item.save()
        


        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def remove_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            cart_item_id = data['cartItemID']
            
            print(cart_item_id)
            
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
        
            cart_item.delete()
            
        except :
            pass
            
        
        return JsonResponse({'success': True})


