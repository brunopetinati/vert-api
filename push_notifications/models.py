from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


class ExpoPushToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

    def __str__(self):
        return self.token


class Notification(models.Model):
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    message = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
