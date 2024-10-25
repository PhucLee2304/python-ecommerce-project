from rest_framework import serializers
from core.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Serialize all fields of the Product model
        
class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested serializer to include product info

    class Meta:
        model = Item
        fields = ['itemID', 'product', 'size', 'stockQuantity']
        
class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)  # Nested serializer to include item info
    item_id = serializers.IntegerField(write_only=True)  # To handle adding items by ID

    class Meta:
        model = CartItem
        fields = ['cart', 'item', 'item_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)  # Include related cart items

    class Meta:
        model = Cart
        fields = ['cartID', 'user', 'totalAmount', 'cart_items']
