from rest_framework import serializers
from .models import Notification, ExpoPushToken


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["icon", "title", "message"]


class ExpoPushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpoPushToken
        fields = ["user", "token"]
