from django.urls import path

from .views import (NotificationCreate, NotificationDelete, NotificationList,
                    NotificationUpdate, SendNotification,
                    UpdateExpoPushTokenView)

urlpatterns = [
    path("notifications/", NotificationList.as_view(), name="notifications-list"),
    path(
        "update-expo-push-token/",
        UpdateExpoPushTokenView.as_view(),
        name="update-expo-push-token",
    ),
    path("send-notification/", SendNotification.as_view(), name="send-notification"),
    path(
        "notifications/create/",
        NotificationCreate.as_view(),
        name="notification-create",
    ),
    path(
        "notifications/<int:id>/",
        NotificationUpdate.as_view(),
        name="notification-update",
    ),
    path(
        "notifications/<int:id>/delete/",
        NotificationDelete.as_view(),
        name="notification-delete",
    ),
]
