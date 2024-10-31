from django.urls import path
from . import views  

urlpatterns = [
    path('', views.payment, name='payment'),
    # path('payment/', views.payment, name='payment'),
    # path('scan/', views.scan, name='scan'),
]