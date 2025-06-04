from django.db import models
from managementactivity.models import TimeStampModel
from posmaster.models import PaymentMethod, UnitMaster, GeneralSettings


# Create your models here.

class UnitPaymentMethod(TimeStampModel):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    unit = models.ForeignKey(UnitMaster, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "unit payment methods"
        ordering = ['-created_at']
        db_table = 'unit_payment_methods'

    def __str__(self):
        return self.value


class UnitGeneralSettings(TimeStampModel):
    general_settings = models.ForeignKey(GeneralSettings, on_delete=models.CASCADE)
    unit = models.ForeignKey(UnitMaster, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "unit general settings"
        ordering = ['-created_at']
        db_table = 'unit_general_settings'

    def __str__(self):
        return self.value
