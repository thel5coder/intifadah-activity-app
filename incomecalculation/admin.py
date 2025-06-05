from django.contrib import admin
from managementactivity.models import MasterIncome
from incomecalculation.models import ManagerialFixIncome

admin.site.register(MasterIncome)
admin.site.register(ManagerialFixIncome)