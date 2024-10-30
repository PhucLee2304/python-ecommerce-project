from django.urls import path
from . import views  
app_name="purchase"

urlpatterns = [
    path('', views.payment, name='payment'),
    
]