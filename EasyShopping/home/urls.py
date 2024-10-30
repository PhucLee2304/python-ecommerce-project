from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:categoryID>/', views.categoryProducts, name='categoryProducts'),
    path('search/', views.search, name='search'),
]