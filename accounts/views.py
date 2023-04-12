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
                          CustomUserSerializer, CustomUserUpdateSerializer, CustomUpdateUserSerializer)
from django.contrib.auth.hashers import check_password

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
                "city": user.city
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
