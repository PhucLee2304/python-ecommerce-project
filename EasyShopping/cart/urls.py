from django.urls import path
from . import views  

urlpatterns = [
    path('cartShow/', views.cartShow, name='cartShow'),
    path('cartActions/', views.cartActions, name='cartActions'),
    path('purchase/', views.purchase, name='purchase'),
]