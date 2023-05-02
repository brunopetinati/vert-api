import socket
import argon2
import dns.resolver
import sys
from django.contrib.auth import authenticate, get_user_model, hashers
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import CustomUserLoginSerializer

from .models import CustomUser
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomUpdateUserSerializer,
    CustomUserEmailPasswordSerializer,
    CustomUserPasswordSerializer,
    CustomUserSerializer,
    CustomUserUpdateSerializer,
)


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

        """ if not password:
            return Response(
                {"error": "Please provide a password"}, 
                status=status.HTTP_400_BAD_REQUEST
            ) """

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Verify the password
        if not check_password(password, user.password):
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
                "email": user.email,
                "user_type": user.user_type,
                "rg": user.rg,
                "cpf": user.cpf,
                "cnpj": user.cnpj,
                "cep": user.cep,
                "street": user.street,
                "number": user.number,
                "complement": user.complement,
                "district": user.district,
                "state": user.state,
                "city": user.city,
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
    serializer_class = CustomUpdateUserSerializer
    lookup_field = "id"


class CustomUserPasswordAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUpdateUserSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        serializer = CustomUserPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object()
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(current_password):
                return Response(
                    {"error": "Invalid current password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response({"success": True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import dns.resolver
import socket

class CustomUserEmailPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserEmailPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User with provided email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate a random password
            new_password = get_random_string(length=8)

            # Hash the password
            hashed_password = hashers.make_password(new_password)

            # Update the user's password in the database
            user.password = hashed_password
            user.save()

            # Resolve the hostname of the SMTP server
            try:
                smtp_host = socket.gethostbyname('your-smtp-hostname-here')
            except socket.gaierror:
                return Response(
                    {"error": "Failed to resolve SMTP host. Please check your internet connection and try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Send the new password to the user via email
            try:
                send_mail(
                    "Your new password",
                    f"Your new password is: {new_password}",
                    "from@example.com",
                    [email],
                    fail_silently=False,
                    connection=smtp_host,
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response({"success": True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
