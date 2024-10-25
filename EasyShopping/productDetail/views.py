
from rest_framework import viewsets
from core.models import *
from .serializers import ProductSerializer
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import F
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'productID'  # Retrieve by productID instead of default 'id'


def productDetailView(request, pid):
    product = Product.objects.get(productID = pid)
    print(product.items.all())
    context = {
        "product" : product
    }
    return render(request, 'productDetail/index.html', context)




    
# views.py


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access cart

    def get_queryset(self):
        # Only return the cart of the logged-in user
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handle adding items to the cart. If the item already exists in the cart, update its quantity.
        """
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)  # Ensure the user has a cart
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)
        print(item_id)

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        cart_item.quantity += int(quantity)  # Increase the quantity if it exists
        cart_item.save()

        # Update total amount
        cart.totalAmount += item.product.getNewPrice() * int(quantity)
        cart.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
