import argon2
import dns.resolver
import jwt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import (PasswordResetTokenGenerator,
                                        default_token_generator)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BankInfo, CustomUser, UserSettings, UserTypeEnum
from .serializers import (BankInfoSerializer, CustomTokenObtainPairSerializer,
                          CustomUpdateUserSerializer,
                          CustomUserEmailPasswordSerializer,
                          CustomUserLoginSerializer,
                          CustomUserPasswordSerializer, CustomUserSerializer,
                          UserSettingsSerializer)


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


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Usuário com o email fornecido não existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate the password reset token
        token = default_token_generator.make_token(user)

        # Convert the user's id to bytes, then encode it in base64
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Build the password reset URL
        current_site = get_current_site(request)
        reset_url = (
            f"https://plataforma.vertecotech.com/recover_password/{uidb64}/{token}/"
        )

        # Compose the email body
        email_body = f"Clique no seguinte link para redefinir sua senha:\n\n{reset_url}"

        # Send the password reset email
        send_mail(
            "Redefinir sua senha",
            email_body,
            "noreply@mysite.com",
            [user.email],
        )

        return Response(
            {"message": "Enviamos por email as instruções para definir sua senha."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            # Here we handle the possible UnicodeDecodeError
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
            except UnicodeDecodeError:
                raise AuthenticationFailed("Invalid uidb64.")

            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                password = request.data.get("password")
                password2 = request.data.get("password2")

                if password == password2:
                    user.set_password(password)
                    user.save()
                    return Response(
                        {"message": "Password reset successful."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Passwords do not match."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Invalid uidb64 or token.")


class BankInfoListAPIView(generics.ListAPIView):
    """
    API endpoint that allows users to list all bank information.
    """

    queryset = BankInfo.objects.all()
    serializer_class = BankInfoSerializer


class BankInfoCreateAPIView(generics.CreateAPIView):
    """
    API endpoint that allows users to create their bank information.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankInfoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankInfoRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that allows users to retrieve and update their bank information.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankInfoSerializer

    def get_object(self):
        try:
            return self.request.user.bank_info
        except BankInfo.DoesNotExist:
            return Response(
                {"error": "Bank information not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BankInfoRetrieveByIDAPIView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to retrieve a bank information by ID.
    """

    queryset = BankInfo.objects.all()
    serializer_class = BankInfoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class BankInfoDeleteAPIView(generics.DestroyAPIView):
    queryset = BankInfo.objects.all()
    serializer_class = BankInfoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]


# view de teste para envio de e-mail
def send_email_view(request):
    send_mail(
        "Assunto do email",
        "Corpo do email.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
    return HttpResponse("E-mail enviado!")


class UsersWithoutProjectsView(APIView):
    def get(self, request):
        users_without_projects = CustomUser.objects.filter(project__isnull=True)
        serializer = CustomUserSerializer(users_without_projects, many=True)
        return Response(serializer.data)
