from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class IncomeSettings(TimeStampModel):
    key = models.CharField(max_length=120)
    value = models.DecimalField(decimal_places=2, max_digits=20)
    type = models.CharField(max_length=120)

    class Meta:
        db_table = 'income_settings'
        ordering = ('key',)
        verbose_name_plural = 'Income Settings'

    def __str__(self):
        return self.key