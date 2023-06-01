from django.urls import path
from .views import NotificationList, SendNotification, ExpoPushTokenListCreateView,
    ExpoPushTokenRetrieveUpdateDestroyView

urlpatterns = [
    path('notifications/', NotificationList.as_view(), name='notifications'),
    path('update-expo-push-token/', UpdateExpoPushTokenView.as_view(), name='update-expo-push-token'),
    path('send-notification/', SendNotification.as_view(), name='send-notification'),
]
