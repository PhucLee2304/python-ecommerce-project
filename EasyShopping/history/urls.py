
from django.urls import path
from . import views

urlpatterns = [
    path('order-history/', views.show, name='order-history'),
]