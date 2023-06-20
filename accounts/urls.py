from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BankInfoCreateAPIView, BankInfoDeleteAPIView,
                    BankInfoListAPIView, BankInfoRetrieveByIDAPIView,
                    BankInfoRetrieveUpdateAPIView, CustomUserCreate,
                    CustomUserDeleteAPIView, CustomUserGetByIdAPIView,
                    CustomUserList, CustomUserLoginView,
                    CustomUserPasswordAPIView, CustomUserUpdateAPIView,
                    PasswordResetConfirmView, PasswordResetRequestView,
                    UserSettingsViewSet, UsersWithoutProjectsView)

router = DefaultRouter()
router.register(r"user-settings", UserSettingsViewSet)

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
    # path(
    #     "send-password/<str:email>/",
    #     CustomUserEmailPasswordAPIView.as_view(),
    #     name="send_password",
    # ),
    path("bankinfo/", BankInfoCreateAPIView.as_view(), name="bankinfo-create"),
    path("bankinfo/list/", BankInfoListAPIView.as_view(), name="bankinfo-list"),
    path(
        "bank-info/<int:id>/",
        BankInfoRetrieveByIDAPIView.as_view(),
        name="bank-info-retrieve-by-id",
    ),
    path(
        "bankinfo/<int:id>/",
        BankInfoRetrieveUpdateAPIView.as_view(),
        name="bankinfo-retrieve-update",
    ),
    path(
        "bankinfo/<int:id>/delete/",
        BankInfoDeleteAPIView.as_view(),
        name="bankinfo-delete",
    ),
    path("", include(router.urls)),
    # path("send-email/", send_email_view, name="send_email"),
    path("users_without_projects/", UsersWithoutProjectsView.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
