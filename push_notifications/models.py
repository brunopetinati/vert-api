from django.db import models
from django.conf import settings
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
