from django.urls import path
from .views import CustomUserCreate, CustomUserList, CustomUserLoginView

urlpatterns = [
    path('signup/', CustomUserCreate.as_view(), name="user_create"),
    path('login/', CustomUserLoginView.as_view(), name="token_create"),
    path('users/', CustomUserList.as_view(), name='users-list'),
]