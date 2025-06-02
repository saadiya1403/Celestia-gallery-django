
from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.sign_up, name='register'),
]
