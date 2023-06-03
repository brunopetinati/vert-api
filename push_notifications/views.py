from rest_framework import generics
from .models import Notification, ExpoPushToken
from .serializers import NotificationSerializer, ExpoPushTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from pyfcm import FCMNotification
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model

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


class NotificationCreate(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationUpdate(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'id' 

class NotificationDelete(generics.DestroyAPIView):
    queryset = Notification.objects.all()
    lookup_field = 'id'  


from django.utils import timezone

class SendNotification(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        notification_id = request.data.get("notification_id")
        if not user_id or not notification_id:
            return Response(
                {"error": "user_id e notification_id são obrigatórios"}, status=400
            )

        try:
            token = ExpoPushToken.objects.get(user_id=user_id).token
        except ExpoPushToken.DoesNotExist:
            return Response(
                {"error": "Token de notificação push não encontrado"}, status=400
            )

        try:
            notification = Notification.objects.get(id=notification_id)
            print('noti#####', notification)
        except Notification.DoesNotExist:
            return Response({"error": "Notificação não encontrada"}, status=404)

        # Atualizar a data da notificação para a data atual
        notification.date = timezone.now()
        notification.save()

        # Construir a mensagem push
        message_body = notification.message
        extra_data = {
            "icon": notification.icon,
            "title": notification.title,
            "body": message_body,
            "date": notification.date.isoformat(),
            "created_at": notification.created_at.isoformat(),
        }

        try:
            response = PushClient().publish(
                PushMessage(to=token, body=message_body, data=extra_data)
            )
        except PushServerError as exc:
            # Lidar com erros de formatação/validação
            return Response({"error": "Erro no servidor de push"}, status=500)
        except DeviceNotRegisteredError:
            # Marcar o token push como inativo
            ExpoPushToken.objects.filter(user_id=user_id).update(active=False)
            return Response({"error": "Token push inválido"}, status=400)
        except PushTicketError:
            # Lidar com outros erros específicos da notificação
            return Response({"error": "Erro no envio da notificação"}, status=500)

        if response.status == "ok":
            # Serializar o token de notificação push e a notificação
            token_serializer = ExpoPushTokenSerializer(
                ExpoPushToken.objects.get(user_id=user_id)
            )
            notification_serializer = NotificationSerializer(notification)
            return Response(
                {
                    "success": "Notificação enviada com sucesso",
                    "token": token_serializer.data,
                    "notification": notification_serializer.data,
                }
            )
        else:
            return Response({"error": "Falha ao enviar a notificação"}, status=500)


