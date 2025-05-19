from email.policy import default

from django.db import models
from .utils import ActivityStatus
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import F, Func, ExpressionWrapper
from django.db.models.functions import ExtractMonth


# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActivityType(TimeStampModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'activity_types'
        ordering = ('name',)
        verbose_name_plural = 'Activity Types'

    def __str__(self):
        return self.name


class Users(TimeStampModel):
    phone = models.CharField(unique=True, primary_key=True, max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.phone} ({self.password})"

    class Meta:
        db_table = 'users'
        ordering = ('phone',)
        verbose_name_plural = 'Users'


class MasterIncome(TimeStampModel):
    MonthlyIncome = models.IntegerField()
    PositionIncome = models.IntegerField()
    HistoryIncome = models.IntegerField()
    VariableIncome = models.IntegerField()
    Month = models.IntegerField()
    Year = models.IntegerField()

    def __str__(self):
        return f"{self.MonthlyIncome} {self.PositionIncome} {self.HistoryIncome} {self.VariableIncome}"

    class Meta:
        db_table = 'master_incomes'
        ordering = ('MonthlyIncome',)
        verbose_name_plural = 'Master Incomes'


class ActivityApproval(TimeStampModel):
    ActivityTypeId = models.ForeignKey(ActivityType, on_delete=models.CASCADE, default=1)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'activity_approvals'
        verbose_name_plural = 'Activity Approvals'

    def __str__(self):
        return f"{self.ActivityTypeId} | {self.UserId.first_name}"


class EpochToDateTime(Func):
    function = 'to_timestamp'
    template = "%(function)s(%(expressions)s)"
    output_field = models.DateTimeField()


class EpochQuerySet(models.QuerySet):
    def with_month(self,field):
        return self.annotate(
            datetime_field=ExpressionWrapper(
                EpochToDateTime(F(field)),
                output_field=models.DateTimeField()
            ),
            month=ExtractMonth(F('datetime_field'))
        )


class ManagerialActivity(TimeStampModel):
    ManagerialUser = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    ActivityDetail = models.TextField()
    ActivityResult = models.TextField(null=True)
    ActivityScore = models.IntegerField(null=True)
    ActivityImage = models.ImageField(upload_to='uploads/', default='blank.png', blank=True)
    RejectedReason = models.TextField(null=True)
    ActivityDateTime = models.IntegerField()
    ActivityStatus = models.IntegerField(choices=ActivityStatus.choices, default=ActivityStatus.WAITING_APPROVAL)
    ActivityType = models.ForeignKey(ActivityType, on_delete=models.CASCADE, default=0)
    ApprovedAt = models.IntegerField(null=True)
    ApprovedById = models.IntegerField(null=True)

    objects = EpochQuerySet.as_manager()

    @property
    def activity_epoch_to_datetime(self):
        date_time = datetime.fromtimestamp(self.ActivityDateTime)
        return date_time

    class Meta:
        db_table = 'managerial_activities'
        verbose_name_plural = 'Managerial Activities'
        permissions = [
            ("update_activity_status", "Dapat merubah status aktivitas")
        ]

    def __str__(self):
        return f"{self.ActivityStatus} | {self.ActivityDetail} | {self.ActivityResult} | {self.ManagerialUser.first_name}"
