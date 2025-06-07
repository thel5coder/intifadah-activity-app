from incomecalculation.models import ManagerialIncome, ManagerialFixIncome
from managementactivity.models import MasterIncome, ManagerialActivity
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    total_all_score = 0
    managerial_incomes = []
    master_income = MasterIncome
    month = 0
    total_index = 0
    total_percentage_history = 0
    total_percentage_position = 0

    if request.method == "POST":
        month = request.POST['month']
        master_income = MasterIncome.objects.get(Month=month)
        if month == "0":
            list_of_months = MasterIncome.objects.all()
            return render(request, 'managerialincome/index.html', {'list_of_months': list_of_months})

        instances = ManagerialIncome.objects.all().filter(month=month)
        if len(instances) > 0:
            for instance in instances:
                total_all_score += instance.total_score
                total_index += instance.index
                managerial_incomes.append(ManagerialIncome(index=instance.index, total_score=instance.total_score,
                                                           user_id=instance.user_id,
                                                           variable_income=instance.variable_income,
                                                           history_income=instance.history_income,
                                                           position_income=instance.position_income,
                                                           fix_income=instance.fix_income,
                                                           total_income=instance.total_income,
                                                           month=month))
            for managerial_income in managerial_incomes:
                managerial_income.user_managerial = User.objects.get(id=managerial_income.user_id)
                try:
                    fix_income = ManagerialFixIncome.objects.get(user_id=managerial_income.user_id)
                    total_percentage_history += fix_income.history_income_percentage
                    total_percentage_position += fix_income.position_income_percentage
                except ObjectDoesNotExist:
                    fix_income = None

                managerial_income.fix_income_var = fix_income

            total_variable_income = (master_income.VariableIncome / 100) * master_income.MonthlyIncome
            print(Decimal(str((master_income.HistoryIncome / 100))))
            history_income = Decimal(str((master_income.HistoryIncome / 100))) * master_income.MonthlyIncome
            position_income = Decimal(str((master_income.PositionIncome / 100))) * master_income.MonthlyIncome

            master_income.value_variable_income = total_variable_income
            master_income.value_history_income = history_income
            master_income.value_position_income = position_income

        else:
            q = ManagerialActivity.objects.with_month('ActivityDateTime').filter(
                month=month).filter(ActivityStatus=1)

            this_months = q.values('ManagerialUser_id', 'ManagerialUser_id__first_name').annotate(
                total_score=Sum('ActivityScore')).order_by('ManagerialUser_id', 'total_score')

            for this_month in this_months:
                total_all_score += this_month['total_score']

            # calculate and save
            total_variable_income = (master_income.VariableIncome / 100) * master_income.MonthlyIncome
            print(Decimal(str((master_income.HistoryIncome / 100))))
            history_income = Decimal(str((master_income.HistoryIncome / 100))) * master_income.MonthlyIncome
            position_income = Decimal(str((master_income.PositionIncome / 100))) * master_income.MonthlyIncome
            master_income.value_variable_income = total_variable_income
            master_income.value_history_income = history_income
            master_income.value_position_income = position_income
            exclude_user_ids = []
            for this_month in this_months:
                # variable income calculation
                index_score = round(this_month['total_score'] / total_all_score * 100, 2)
                variable_income = round((index_score / 100) * total_variable_income, 2)
                total_index += index_score
                # end variable income calculation

                # fix income calculation
                try:
                    fix_income = ManagerialFixIncome.objects.get(user_id=this_month['ManagerialUser_id'])
                    total_percentage_history += fix_income.history_income_percentage
                    total_percentage_position += fix_income.position_income_percentage
                    managerial_history_income = round((fix_income.history_income_percentage / 100) * history_income, 2)
                    managerial_position_income = round((fix_income.position_income_percentage / 100) * position_income)
                    total_fix_income = round(managerial_position_income + managerial_history_income, 2)
                    exclude_user_ids.append(this_month['ManagerialUser_id'])
                except ObjectDoesNotExist:
                    managerial_history_income = 0
                    managerial_position_income = 0
                    total_fix_income = 0
                # end fix income calculation

                total_income = Decimal(str(total_fix_income)) + Decimal(str(variable_income))
                managerial_incomes.append(ManagerialIncome(index=index_score, total_score=this_month['total_score'],
                                                           user_id=this_month['ManagerialUser_id'],
                                                           variable_income=round(variable_income, 0),
                                                           history_income=managerial_history_income,
                                                           position_income=managerial_position_income,
                                                           fix_income=total_fix_income, total_income=total_income,
                                                           month=month))

            # only fix income no variable income
            only_fix_incomes = ManagerialFixIncome.objects.exclude(user_id__in=exclude_user_ids)
            for only_fix_income in only_fix_incomes:
                variable_income = 0
                total_percentage_history += only_fix_income.history_income_percentage
                total_percentage_position += only_fix_income.position_income_percentage
                managerial_history_income = round((only_fix_income.history_income_percentage / 100) * history_income, 2)
                managerial_position_income = round((only_fix_income.position_income_percentage / 100) * position_income)
                total_fix_income = round(managerial_position_income + managerial_history_income, 2)

                total_income = total_fix_income + variable_income
                managerial_incomes.append(ManagerialIncome(index=0, total_score=0,
                                                           user_id=only_fix_income.user_id,
                                                           variable_income=0,
                                                           history_income=managerial_history_income,
                                                           position_income=managerial_position_income,
                                                           fix_income=total_fix_income, total_income=total_income,
                                                           month=month))

            ManagerialIncome.objects.bulk_create(managerial_incomes)

            for managerial_income in managerial_incomes:
                fix_income = ManagerialFixIncome.objects.get(user_id=this_month['ManagerialUser_id'])
                managerial_income.user_managerial = User.objects.get(id=managerial_income.user_id)
                managerial_income.fix_income_var = fix_income

    list_of_months = MasterIncome.objects.all()

    return render(request, 'managerialincome/index.html',
                  {'list_of_months': list_of_months, 'total_score': total_all_score,
                   'managerial_incomes': managerial_incomes, 'master_income': master_income,
                   'total_index': total_index, 'month': month, 'total_percentage_history': total_percentage_history,
                   'total_percentage_position': total_percentage_position})
