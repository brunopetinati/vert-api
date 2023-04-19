import argon2
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import authenticate, hashers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.authentication import (BasicAuthentication, SessionAuthentication)
from rest_framework.decorators import (authentication_classes, permission_classes)
from rest_framework.permissions import (AllowAny, BasePermission, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from accounts.serializers import CustomUserLoginSerializer
from .serializers import (CustomTokenObtainPairSerializer, CustomUserSerializer, CustomUserUpdateSerializer, CustomUpdateUserSerializer)


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

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
        if user.check_password(password):
            # Generate a new password reset token
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            # Set the user's password reset token and send the email
            user.password_reset_token = token
            user.save()
            subject = 'Reset Your Password'
            message = f'Please click on the following link to reset your password: http://example.com/reset-password/{token}'
            from_email = 'noreply@example.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid password'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def recover_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return JsonResponse({'error': 'No user with that email.'}, status=404)
        
        new_password = get_random_string(length=10) # generate new password
        user.set_password(new_password) # set the new password
        user.save() # save the user object
        send_mail(
            'Your new password', # subject
            f'Your new password is: {new_password}', # message
            'from@example.com', # from email
            [email], # recipient email
            fail_silently=False, # raise an error if the email fails to send
        )
        return JsonResponse({'success': 'Password reset email sent.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)