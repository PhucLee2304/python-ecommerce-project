from django.urls import path
from . import views  

urlpatterns = [
    path('', views.showOrder, name='showOrder'),
    
]