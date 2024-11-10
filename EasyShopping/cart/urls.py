from django.urls import path
from . import views  

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('update-cart-item-size/', views.update_cart_item_size, name='update_cart_item_size'),
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),
]