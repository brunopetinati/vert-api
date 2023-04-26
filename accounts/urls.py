from django.urls import path

from .views import (
    CustomUserCreate,
    CustomUserDeleteAPIView,
    CustomUserEmailPasswordAPIView,
    CustomUserGetByIdAPIView,
    CustomUserList,
    CustomUserLoginView,
    CustomUserPasswordAPIView,
    CustomUserUpdateAPIView,
)

urlpatterns = [
    path("signup/", CustomUserCreate.as_view(), name="user_create"),
    path("login/", CustomUserLoginView.as_view(), name="token_create"),
    path("users/", CustomUserList.as_view(), name="users-list"),
    path("users/<int:id>/", CustomUserGetByIdAPIView.as_view(), name="user-detail"),
    path(
        "users/<int:id>/update/", CustomUserUpdateAPIView.as_view(), name="user-update"
    ),
    path(
        "users/<int:id>/delete/", CustomUserDeleteAPIView.as_view(), name="user-delete"
    ),
    path(
        "reset-password/<int:id>/",
        CustomUserPasswordAPIView.as_view(),
        name="reset_password",
    ),
    path(
        "send-password/<int:id>/",
        CustomUserEmailPasswordAPIView.as_view(),
        name="send_password",
    ),
]
