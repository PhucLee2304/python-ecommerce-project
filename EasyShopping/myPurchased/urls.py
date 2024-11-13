from django.urls import path
from . import views  
# app_name = 'myPurchased'


urlpatterns = [
    path('my-purchased/<detail>/', views.myPurchasedView, name='my-purchased'),
    path('cancel-order/<oid>/', views.cancelView, name='cancel-order'),
]