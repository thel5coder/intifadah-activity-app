from xml.dom import ValidationErr

from django.shortcuts import render, redirect
from incomecalculation.models import IncomeSettings
from .form import IncomeSettingForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
import json


def index(request):
    income_settings = IncomeSettings.objects.all().order_by('id')

    return render(request, 'incomesetting/list.html', {'income_settings': income_settings})


def create(request):
    income_settings = IncomeSettings()
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data['key'] == "" or data['val'] == "" or data['type'] == "":
            error = {"message": "Form harus di isi semua", "is_error": True}
            return JsonResponse({'error': error}, status=400)
        else:
            try:
                if IncomeSettings.objects.filter(key=data['key']).count() > 0:
                    return JsonResponse({'error': 'Key sudah ada dalam data'}, status=400)

                income_settings.key = data['key']
                income_settings.value = data['val']
                income_settings.type = data['type']
                income_settings.save()
                return JsonResponse({}, status=200)
            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    else:
        form = IncomeSettingForm()

    return render(request, 'incomesetting/create.html', {'forms': form})


def read(request, income_setting_id):
    income_setting = IncomeSettings.objects.get(id=income_setting_id)
    form = IncomeSettingForm(instance=income_setting)

    return render(request, 'incomesetting/update.html', {'income_setting': income_setting, 'form': form})
    # try:

    # except ValidationError as e:
    #     return JsonResponse({'error': str(e)}, status=400)
    # except IncomeSettings.DoesNotExist as e:
    #     return JsonResponse({'error': str(e)}, status=400)
    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=500)


def update(request, income_setting_id):
    income_settings = IncomeSettings.objects.get(id=income_setting_id)
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if data['key'] == "" or data['val'] == "" or data['type'] == "":
            error = {"message": "Form harus di isi semua", "is_error": True}
            return JsonResponse({'error': error}, status=400)
        else:
            try:
                if IncomeSettings.objects.filter(key=data['key']).count() > 0:
                    return JsonResponse({'error': 'Key sudah ada dalam data'}, status=400)
                income_settings.key = data['key']
                income_settings.value = data['val']
                income_settings.type = data['type']
                income_settings.save()
                return JsonResponse({}, status=200)
            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    return None


def delete(request, income_setting_id):
    income_settings = IncomeSettings.objects.get(id=income_setting_id)
    if request.method == 'DELETE':
        try:
            income_settings.delete()
            return JsonResponse({}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return None
