from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'phone', 'city', 'state', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['id'] = self.user.id
#         data['full_name'] = self.user.full_name
#         data['phone'] = self.user.phone
#         data['city'] = self.user.city
#         data['state'] = self.user.state
#         return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adicione quaisquer outros campos que você deseja incluir no payload do token
        token['email'] = user.email
        return token

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        # Certifique-se de que o email seja exclusivo para cada usuário, caso contrário, pode haver vários usuários com o mesmo email
        user = authenticate(request=self.context['request'], **credentials)
        if not user:
            raise AuthenticationFailed('Credenciais inválidas.')
        if not user.is_active:
            raise AuthenticationFailed('Conta desativada ou excluída.')
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
