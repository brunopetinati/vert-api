from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, BankInfo, UserTypeEnum, UserSettings


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name",
            "rg",
            "cpf",
            "phone",
            "cep",
            "cnpj",
            "street",
            "number",
            "district",
            "complement",
            "city",
            "state",
            "email",
            "user_type",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name",
            "rg",
            "cpf",
            "phone",
            "cep",
            "cnpj",
            "street",
            "number",
            "district",
            "complement",
            "city",
            "state",
            "email",
            "user_type",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.rg = validated_data.get("rg", instance.rg)
        instance.cpf = validated_data.get("cpf", instance.cpf)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.cep = validated_data.get("cep", instance.cep)
        instance.cnpj = validated_data.get("cnpj", instance.cnpj)
        instance.street = validated_data.get("street", instance.street)
        instance.number = validated_data.get("number", instance.number)
        instance.district = validated_data.get("district", instance.district)
        instance.complement = validated_data.get("complement", instance.complement)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.user_type = validated_data.get("user_type", instance.user_type)
        instance.save()

        return instance


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



class CustomUserPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )


class CustomUserEmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()



class BankInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for bank information of CustomUser.
    """
    account_type = serializers.CharField(max_length=2)

    class Meta:
        model = BankInfo
        fields = ["id", "account_type", "bank", "account_number", "agency", "pix_key", "user"]

    def create(self, validated_data):
        account_type = validated_data.pop("account_type")
        user = validated_data.pop("user")
        bank_information = BankInfo.objects.create(account_type=account_type, user=user, **validated_data)
        return bank_information

    def update(self, instance, validated_data):
        instance.account_type = validated_data.get("account_type", instance.account_type)
        instance.bank = validated_data.get("bank", instance.bank)
        instance.account_number = validated_data.get("account_number", instance.account_number)
        instance.agency = validated_data.get("agency", instance.agency)
        instance.pix_key = validated_data.get("pix_key", instance.pix_key)
        instance.save()
        return instance



class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['user', 'style_cards_users', 'style_cards_projects']

    def create(self, validated_data):
        user_settings = UserSettings.objects.create(**validated_data)
        return user_settings

    def update(self, instance, validated_data):
        instance.style_cards_users = validated_data.get('style_cards_users', instance.style_cards_users)
        instance.style_cards_projects = validated_data.get('style_cards_projects', instance.style_cards_projects)
        instance.save()
        return instance
