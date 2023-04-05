from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "rg", "cpf", "phone", "street", "number", "district", "complement", "city", "state", "email", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(
                request=self.context["request"], email=email, password=password
            )
            if not user:
                raise AuthenticationFailed("Credenciais inválidas.")
            if not user.is_active:
                raise AuthenticationFailed("Conta desativada ou excluída.")
            data = {
                "id": user.id,
                "full_name": user.full_name,
                "phone": user.phone,
                "city": user.city,
                "state": user.state,
                "email": user.email,
                "user_type": user.user_type,
                "refresh": str(self.get_token(user)),
                "access": str(self.get_token(user).access_token),
            }
            return data
        else:
            raise AuthenticationFailed("Informe o email e a senha.")





# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ["id", "full_name", "phone", "city", "state", "email"]


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "phone", "cpf", "cep", "street", "number", "complement", "district","city", "state", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        # verifique se o valor do campo de email foi alterado
        if 'email' in validated_data and validated_data['email'] != instance.email:
            # verifique se o novo valor do campo de email já existe em outro registro
            if CustomUser.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Este email já está em uso.")

        # atualize o objeto `CustomUser` com os dados validados
        return super().update(instance, validated_data)