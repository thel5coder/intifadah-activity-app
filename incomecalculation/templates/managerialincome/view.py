from incomecalculation.models import ManagerialIncome
from managementactivity.models import MasterIncome, ManagerialActivity
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.contrib.auth.models import User


def index(request):
    total_all_score = 0
    managerial_incomes = []
    if request.method == "POST":
        month = request.POST['month']
        if month == "0":
            list_of_months = MasterIncome.objects.all()
            return render(request, 'managerialincome/index.html', {'list_of_months': list_of_months})

        instances = ManagerialIncome.objects.all().filter(month=month)
        if len(instances) > 0:
            for instance in instances:
                managerial_incomes.append(ManagerialIncome(index=instance.index, total_score=instance.total_score,
                                                           user_id=instance.user_id,
                                                           variable_income=instance.variable_income, history_income=0,
                                                           position_income=0, fix_income=0, total_income=0,
                                                           month=month))
            for managerial_income in managerial_incomes:
                managerial_income.user_managerial = User.objects.get(id=managerial_income.user_id)

        else:
            # get data needed
            master_income = MasterIncome.objects.get(Month=month)

            q = ManagerialActivity.objects.with_month('ActivityDateTime').filter(
                month=month).filter(ActivityStatus=1)

            this_months = q.values('ManagerialUser_id', 'ManagerialUser_id__first_name').annotate(
                total_score=Sum('ActivityScore')).order_by('ManagerialUser_id', 'total_score')

            for this_month in this_months:
                total_all_score += this_month['total_score']
                print(this_month)

            # calculate and save
            total_variable_income = (master_income.VariableIncome / 100) * master_income.MonthlyIncome
            for this_month in this_months:
                index_score = round(this_month['total_score'] / total_all_score * 100, 2)
                variable_income = (index_score / 100) * total_variable_income
                managerial_incomes.append(ManagerialIncome(index=index_score, total_score=this_month['total_score'],
                                                           user_id=this_month['ManagerialUser_id'],
                                                           variable_income=round(variable_income, 0), history_income=0,
                                                           position_income=0, fix_income=0, total_income=0,
                                                           month=month))
            ManagerialIncome.objects.bulk_create(managerial_incomes)

            for managerial_income in managerial_incomes:
                managerial_income.user_managerial = User.objects.get(id=managerial_income.user_id)

    list_of_months = MasterIncome.objects.all()
    return render(request, 'managerialincome/index.html',
                  {'list_of_months': list_of_months, 'total_score': total_all_score,
                   'managerial_incomes': managerial_incomes})
