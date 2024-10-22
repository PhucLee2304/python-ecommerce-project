# from django.shortcuts import render, redirect
# from .models import Cart, CartItem
# from account.models import Customer
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# @login_required(login_url='login')
# def cartShow(request):
#     cart = Cart.objects.filter(customer=request.user.customer).first()
#     items = []
#     totalAmount = 0

#     if cart:
#         cartItems = CartItem.objects.filter(cart=cart)
#         if not cartItems:
#             messages.info(request, "Your cart is empty")
#     else:
#         messages.info(request, "Your cart is empty")
#         cartItems = []

#     for cartItem in cartItems:
#         product = cartItem.item.product
#         size = cartItem.item.size
#         priceAfterDiscount = round(product.price * (1 - product.discount))
#         totalPrice = cartItem.quantity * priceAfterDiscount 
#         item = {
#             'itemID': cartItem.item.itemID,
#             'productName': product.productName,
#             'productImage': f"/media/products/{product.productImage}",
#             'sizeName': size.sizeName,
#             'price': product.price,
#             'priceAfterDiscount': priceAfterDiscount,
#             'discount': product.discount,
#             'quantity': cartItem.quantity,
#             'totalPrice': totalPrice,
#             # 'shippingFee': product.shippingFee,
#         }
#         items.append(item)
#         totalAmount += totalPrice

#     context = { 
#         'items': items,
#         'totalAmount': totalAmount,
#     }
#     return render(request, 'cart.html', context)

# @login_required(login_url='login')
# def cartActions(request):
#     cart = Cart.objects.filter(customer=request.user.customer).first()

#     if request.method == 'POST':
#         if 'deleteProduct' in request.POST:
#             itemID = request.POST.get('deleteProduct')
#             try:
#                 cartItem = CartItem.objects.get(cart=cart, item__itemID=itemID)
#                 cartItem.delete()
#                 return redirect('cartShow')
#             except CartItem.DoesNotExist:
#                 messages.info(request, "Item not found in cart")
        
#         elif 'deleteAll' in request.POST:
#             if cart:
#                 CartItem.objects.filter(cart=cart).delete()
#                 return redirect('cartShow')
        
#         elif 'buyAll' in request.POST:
#             items = []
#             selectedItems = request.POST.getlist('selectProduct[]')

#             if not selectedItems:
#                 return redirect('cartShow')  

#             for i in range(1, len(request.POST) // 2 + 1):
#                 itemID = request.POST.get(f'itemID{i}')
#                 if itemID in selectedItems:
#                     item = {
#                         'itemID': itemID,
#                         'quantity': int(request.POST.get(f'quantity{i}')),
#                     }
#                     items.append(item)   

#             context = {
#                 'items': items,
#             }
#             return render(request, 'purchase.html', context)
 
#     return redirect('cartShow')

# # @login_required(login_url='login')
# # def purchase(request):
# #     return render(request, 'purchase.html')
