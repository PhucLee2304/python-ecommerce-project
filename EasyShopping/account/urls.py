from django.urls import path
from . import views  

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('sendToEmail/', views.sendToEmail, name='sendToEmail'),
    path('resetPassword/<uidb64>/<token>/', views.resetPassword, name='resetPassword'),
]