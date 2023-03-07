from django.db import models
from accounts.models import CustomUser

class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_area = models.FloatField()
    legal_reserve_area = models.FloatField()
    address = models.CharField(max_length=255)
    documentation_up_to_date = models.BooleanField()
    status_car = models.CharField(max_length=50)
    sicar_code = models.CharField(max_length=20)
    matricula_status = models.CharField(max_length=20)
    georeferencing_status = models.CharField(max_length=20)
    reserve_legal_status = models.CharField(max_length=50)
    physical_or_legal_entity = models.CharField(max_length=20)
    cnpj = models.IntegerField(null=True)
    conservation_unit = models.CharField(max_length=50)
    owner_actions_to_preserve_forest = models.TextField()
    pdf_matricula_certificate = models.FileField(upload_to='matricula_certificate/')
    pdf_car = models.FileField(upload_to='car/')
    property_polygon = models.FileField(upload_to='property_polygon/')
    pdf_federal_debt_certificate = models.FileField(upload_to='federal_debt/')
    pdf_ccir = models.FileField(upload_to='ccir/')
