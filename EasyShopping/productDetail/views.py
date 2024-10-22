from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
import random
from productDetail.models import Size, Item
from home.models import *
from django.contrib.auth.decorators import login_required
from cart.models import *


# Create your views here.
class ProductDetailView(View):
    def get(self, request, **kwargs):
        product = models.Product.objects.filter(productID = int(kwargs.get('id')))
        product = product[0]
        
        # Get all sizes associated with this product
        sizes = Size.objects.filter(item__product=product)
        
        # relatedProduct = models.Product.objects.filter(category = product.category)
        # se = set()
        # for i in range(len(relatedProduct)):
        #     randIndex = random.randint(0)
            
        # print(relatedProduct)
        context = {
            "product" : product,
            "sizes": sizes,
            'message' : "hello"
        }
        return render(request, 'productDetail/index.html', context)
    
def product_detail_view(request, pid):
    product = Product.objects.get(productID = pid)
    items = product.product.all()
    context= {
        "product" : product,
        "items": items,
    }
    return render(request, "productDetail/index.html", context)

def add_to_cart(request, productID, sizeID):
    item = get_object_or_404(Item, product=Product.objects.get(productID = productID), size=Size.objects.get(sizeID = sizeID))
    cart, created = Cart.objects.get_or_create(user=request.user)
    print(request.user)
    # cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    
    # print(request.user.customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        # If the cart item already exists, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Update the total amount in the cart
    # cart.update_total()

    # return redirect('home:show'
    return render(request, "productDetail/index.html")
    