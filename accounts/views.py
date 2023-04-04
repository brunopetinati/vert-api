import argon2
from django.contrib.auth import authenticate, hashers
from rest_framework import generics, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework.permissions import (AllowAny, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import CustomUserLoginSerializer

from .models import CustomUser
from .serializers import (CustomTokenObtainPairSerializer,
                          CustomUserSerializer, CustomUserUpdateSerializer)


@authentication_classes([])
@permission_classes([])
class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class CustomUserLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    hasher = argon2.PasswordHasher()

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken.for_user(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "id": user.id,
                "full_name": user.full_name,
                "phone": user.phone,
                "city": user.city,
                "state": user.state,
                "email": user.email,
                "user_type": user.user_type,
            }

            return Response(data, status=status.HTTP_200_OK)
        except argon2.exceptions.VerifyMismatchError:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class CustomUserGetByIdAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "id"

class CustomUserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "id"


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserUpdateSerializer
    lookup_field = "id"
