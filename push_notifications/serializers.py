from rest_framework import serializers

from .models import ExpoPushToken, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "icon", "title", "message", "date", "created_at"]


class ExpoPushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpoPushToken
        fields = ["user", "token"]
