from django.db import models


# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UnitMaster(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'units'
        ordering = ('name',)
        verbose_name_plural = 'units'

    def __str__(self):
        return self.name


class PaymentMethod(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'payment_methods'
        ordering = ('name',)
        verbose_name_plural = 'payment methods'

    def __str__(self):
        return self.name

