from django.contrib import admin
from .models import ActivityType,ActivityApproval,ManagerialActivity

# Register your models here.
admin.site.register(ActivityType)
admin.site.register(ActivityApproval)
admin.site.register(ManagerialActivity)

