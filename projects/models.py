from django.db import models

from accounts.models import CustomUser


class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_area = models.FloatField(blank=True)
    legal_reserve_area = models.FloatField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    status_car = models.CharField(max_length=50, blank=True)
    sicar_code = models.CharField(max_length=20, blank=True)
    matricula_status = models.CharField(max_length=20, blank=True)
    georeferencing_status = models.CharField(max_length=20, blank=True)
    reserve_legal_status = models.CharField(max_length=50, blank=True)
    physical_or_legal_entity = models.CharField(max_length=20, blank=True)
    cnpj = models.IntegerField(null=True, blank=True)
    conservation_unit = models.CharField(max_length=50, blank=True)
    owner_actions_to_preserve_forest = models.TextField(blank=True)
    legal_reserve_deficit = models.BooleanField(null=True, blank=True)
    has_federal_debt = models.BooleanField(null=True, blank=True)
    pdf_matricula_certificate = models.FileField(upload_to="matricula_certificate/", blank=True, null=True)
    pdf_car = models.FileField(upload_to="car/", blank=True, null=True)
    property_polygon = models.FileField(upload_to="property_polygon/", blank=True, null=True)
    pdf_federal_debt_certificate = models.FileField(upload_to="federal_debt/", blank=True, null=True)
    pdf_ccir = models.FileField(upload_to="ccir/", blank=True, null=True)

