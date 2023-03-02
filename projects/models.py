from django.db import models
from accounts.models import CustomUser

STATUS_CHOICES = [
   ('Ativo', 'Ativo'),
    ('Pendente', 'Pendente'),
    ('Cancelado', 'Cancelado'),
    ('', 'Não possui'),
]

class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_area = models.FloatField()
    legal_reserve_area = models.FloatField()
    has_matricula_certificate = models.BooleanField()
    pdf_matricula_certificate = models.FileField(upload_to='matricula_certificate/')
    address = models.CharField(max_length=255)
    documentation_up_to_date = models.BooleanField()
    has_car = models.BooleanField()
    status_car = models.CharField(max_length=10, choices=STATUS_CHOICES, default='')
    sicar_code = models.CharField(max_length=20)
    pdf_car = models.FileField(upload_to='car/')
    matricula_status = models.CharField(max_length=20)
    georeferencing_status = models.CharField(max_length=20)
    has_georeferencing_file = models.BooleanField()
    property_polygon = models.FileField(upload_to='property_polygon/')
    reserve_legal_status = models.CharField(max_length=50)
    has_reserve_legal_deficit = models.BooleanField()
    physical_or_legal_entity = models.CharField(max_length=20)
    cnpj = models.IntegerField(null=True)
    conservation_unit = models.CharField(max_length=50)
    federal_debt = models.BooleanField()
    pdf_federal_debt_certificate = models.FileField(upload_to='federal_debt/')
    has_updated_ccir = models.BooleanField()
    pdf_ccir = models.FileField(upload_to='ccir/')
    owner_actions_to_preserve_forest = models.TextField()
