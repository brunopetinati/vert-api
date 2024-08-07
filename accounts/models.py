from django.contrib.auth.models import AbstractUser
from django.db import models


class UserTypeEnum(models.TextChoices):
    REGULAR = "Regular", ("Regular")
    ADMIN = "ADM", ("Admin")
    COMERCIAL = "COM", ("Comercial")
    ENGENHARIA = "ENG", ("Engenharia")


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    rg = models.CharField(max_length=200, blank=True, null=True)
    cpf = models.CharField(max_length=200, blank=True, null=True)
    cnpj = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20)
    complement = models.CharField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=200, blank=True, null=True)
    cep = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserTypeEnum.choices,
        default=UserTypeEnum.REGULAR,
    )
    accept_terms_of_use = models.BooleanField(blank=True, null=True)
    accept_privacy_politics = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # adicionando related_name nos campos de grupos e permissões
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class BankInfo(models.Model):
    ACCOUNT_TYPE = [
        ("PJ", "Pessoa Jurídica"),
        ("PF", "Pessoa Física"),
    ]
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="bank_info"
    )
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPE)
    bank = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    agency = models.CharField(max_length=20)
    pix_key = models.CharField(max_length=100)


class UserSettings(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user_settings"
    )
    style_cards_users = models.BooleanField(default=False)
    style_cards_projects = models.BooleanField(default=False)
