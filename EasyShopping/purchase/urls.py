from django.urls import path
from . import views  

urlpatterns = [
    # path('', views.payment, name='payment'),
    # path('cashOnDelivery/', views.cashOnDelivery, name='cashOnDelivery'),
    # path('bankTransfer/', views.bankTransfer, name='bankTransfer'),
    path('payment/', views.payment, name='payment'),
    path('scan/', views.scan, name='scan'),
    # path('checkout/', views.checkoutView, name='checkout'),
]