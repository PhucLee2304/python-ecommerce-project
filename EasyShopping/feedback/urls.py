from django.urls import path
from . import views  

urlpatterns = [
    path('feedback/<oid>/', views.feedbackView, name='feedback'),
    path('api/submit-feedback/', views.submit_feedback, name="submit-feedback"),
]