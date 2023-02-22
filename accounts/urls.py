from django.urls import path
from .views import UserCreate

urlpatterns = [
    path('users/', UserCreate.as_view()),
]