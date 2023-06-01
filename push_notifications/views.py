from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer, ExpoPushTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from .models import ExpoPushToken
from pyfcm import FCMNotification


class UpdateExpoPushTokenView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user")
        expo_push_token = request.data.get("token")

        if not user_id or not expo_push_token:
            return Response(
                {"error": "user_id and expo_push_token are required"}, status=400
            )

        try:
            user = CustomUser.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        expo_push_token_instance, created = ExpoPushToken.objects.update_or_create(
            user=user, defaults={"token": expo_push_token}
        )

        serializer = ExpoPushTokenSerializer(expo_push_token_instance)
        return Response(serializer.data)


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class SendNotification(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        notification_id = request.data.get("notification_id")

        if not user_id or not notification_id:
            return Response(
                {"error": "user_id and notification_id are required"}, status=400
            )

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        try:
            notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)

        # Construir o payload da notificação
        message_title = notification.title
        message_body = notification.message
        data_message = {
            "icon": notification.icon,
            "title": message_title,
            "body": message_body,
        }

        # Configurar as credenciais do Firebase Cloud Messaging (FCM)
        api_key = "your_fcm_api_key"
        push_service = FCMNotification(api_key=api_key)

        # Enviar a notificação push para o token do usuário
        registration_id = user.expo_push_token.token
        result = push_service.notify_single_device(
            registration_id=registration_id, data_message=data_message
        )

        if result["success"] == 1:
            return Response({"success": "Notification sent successfully"})
        else:
            return Response({"error": "Failed to send notification"}, status=500)
