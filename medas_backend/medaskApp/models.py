from django.db import models


class CompanyInsurance(models.Model):
    company_name = models.CharField(max_length=100)
    insurance_type = models.BooleanField(null=False)  # 0 - ОМС; 1 - ДМС
    insurance_number_type = models.CharField(max_length=50)

    class Meta:
        unique_together = ('insurance_type', 'company_name')
