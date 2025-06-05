from django.db import models
from django.contrib.auth.models import User


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


class ManagerialIncome(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.FloatField()
    total_score = models.DecimalField(decimal_places=0, max_digits=20)
    history_income = models.DecimalField(decimal_places=2, max_digits=20)
    position_income = models.DecimalField(decimal_places=2, max_digits=20)
    fix_income = models.DecimalField(decimal_places=2, max_digits=20)
    variable_income = models.DecimalField(decimal_places=2, max_digits=20)
    total_income = models.DecimalField(decimal_places=2, max_digits=20)
    month = models.DecimalField(decimal_places=0, max_digits=20, default=0)

    class Meta:
        db_table = 'managerial_incomes'
        ordering = ('index',)
        verbose_name_plural = 'Managerial Incomes'

    def __str__(self):
        return self.index

class ManagerialFixIncome(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history_income_percentage = models.FloatField()
    position_income_percentage = models.FloatField()

    class Meta:
        db_table = 'managerial_fix_incomes'
        ordering = ('id',)
        verbose_name_plural = 'Managerial Fixed Incomes'

    def __str__(self):
        return self.history_income_percentage