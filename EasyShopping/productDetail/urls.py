# from django.urls import path
# from .views import *

# urlpatterns = [
    # path('show/', views.show, name='show'),
    # path('')
#     path('api/product/<int:productID>/', ProductDetailView.as_view(), name='product-detail'),
# ]

from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include
# app_name = 'productDetail'
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart-item', CartViewSet, basename='cart-item')

urlpatterns = [
    path('api/', include(router.urls)),  # Include all the routes for the ProductViewSet
    path('products/<pid>/', productDetailView, name="product-detail"),
]
