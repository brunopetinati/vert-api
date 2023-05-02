from django.db import models

from accounts.models import CustomUser


class Project(models.Model):
    title = models.CharField(max_length=100, default="default")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_area = models.FloatField(blank=True)
    legal_reserve_area = models.FloatField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    status_car = models.CharField(max_length=200, blank=True)
    sicar_code = models.CharField(max_length=200, blank=True)
    matricula_status = models.CharField(max_length=200, blank=True)
    georeferencing_status = models.CharField(max_length=200, blank=True)
    reserve_legal_status = models.CharField(max_length=200, blank=True)
    physical_or_legal_entity = models.CharField(max_length=200, blank=True)
    cnpj = models.CharField(max_length=200, null=True, blank=True)
    conservation_unit = models.CharField(max_length=200, blank=True)
    owner_actions_to_preserve_forest = models.TextField(blank=True)
    legal_reserve_deficit = models.BooleanField(null=True, blank=True)
    has_federal_debt = models.BooleanField(null=True, blank=True)
    pdf_matricula_certificate = models.FileField(
        upload_to="matricula_certificate/", blank=True, null=True
    )
    pdf_car = models.FileField(upload_to="car/", blank=True, null=True)
    property_polygon = models.FileField(
        upload_to="property_polygon/", blank=True, null=True
    )
    pdf_federal_debt_certificate = models.FileField(
        upload_to="federal_debt/", blank=True, null=True
    )
    pdf_ccir = models.FileField(upload_to="ccir/", blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=60, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_score(self):
        filled_fields = [
            self.total_area,
            self.legal_reserve_area,
            self.address,
            self.status_car,
            self.sicar_code,
            self.matricula_status,
            self.georeferencing_status,
            self.reserve_legal_status,
            self.physical_or_legal_entity,
            self.conservation_unit,
            self.owner_actions_to_preserve_forest,
            self.legal_reserve_deficit,
            self.has_federal_debt,
        ]
        score = sum(1 for field in filled_fields if field)
        score += 3 * sum(
            1
            for field in [
                self.pdf_matricula_certificate,
                self.pdf_car,
                self.property_polygon,
                self.pdf_federal_debt_certificate,
                self.pdf_ccir,
            ]
            if field
        )
        return score

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)
