from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include


urlpatterns = [
    path('products/<pid>/', productDetailView, name="product-detail"),
    path('api/cart-item/', add_to_cart),
]
