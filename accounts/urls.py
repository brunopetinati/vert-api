from django.urls import path
from .views import CustomUserCreate, CustomTokenObtainPairView

urlpatterns = [
    path('signup/', CustomUserCreate.as_view(), name="user_create"),
    path('login/', CustomTokenObtainPairView.as_view(), name="token_create"),
]