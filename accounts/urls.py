from django.urls import path

from .views import (
    CustomUserCreate,
    CustomUserGetByIdAPIView,
    CustomUserList,
    CustomUserLoginView,
)

urlpatterns = [
    path("signup/", CustomUserCreate.as_view(), name="user_create"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_create"),
    path("users/", CustomUserList.as_view(), name="users-list"),
    path("users/<int:id>/", CustomUserGetByIdAPIView.as_view(), name="user-detail"),
]
