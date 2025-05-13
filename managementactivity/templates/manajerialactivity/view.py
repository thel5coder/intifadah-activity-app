from django.shortcuts import render, redirect
from managementactivity.models import ManagerialActivity, ActivityType
from managementactivity.utils import ActivityStatus
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from managementactivity.models import ActivityApproval


def index(request):
    print(request.user.id)
    activities = ManagerialActivity.objects.filter(ManagerialUser_id=request.user.id)
    for activity in activities:
        activity.status = {'value': ActivityStatus.get_key_text(activity.ActivityStatus),
                           'badge': ActivityStatus.get_badge_status(activity.ActivityStatus)}
        formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
        activity.ActivityDateTime = formatted_time

    return render(request, 'manajerialactivity/list.html', {'activities': activities})


def create(request):
    if request.method == 'POST':
        activity = ManagerialActivity()
        activity.ActivityImage = request.FILES['activityImage']
        activity.ActivityDetail = request.POST['activityDetail']
        activity.ActivityResult = request.POST['activityResult']
        activity.ActivityStatus = ActivityStatus.WAITING_APPROVAL
        date_str = request.POST['activityDateTime']
        date_time_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        activity.ActivityDateTime = date_time_obj.timestamp()
        activity.ManagerialUser_id = request.user.id
        activity.ActivityType_id = request.POST['activityType']
        activity.save()
        return redirect('activity-list')

    activityTypes = ActivityType.objects.all()
    return render(request, 'manajerialactivity/create.html', {'activityTypes': activityTypes})


def update(request, activity_id):
    activity = ManagerialActivity.objects.get(id=activity_id)
    if request.method == 'POST':
        activity.ActivityImage = request.FILES['activityImage']
        activity.ActivityDetail = request.POST['activityDetail']
        activity.ActivityResult = request.POST['activityResult']
        date_str = request.POST['activityDateTime']
        date_time_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        activity.ActivityDateTime = date_time_obj.timestamp()
        activity.ActivityType_id = request.POST['activityType']
        activity.save()
        return redirect('activity-list')

    activityTypes = ActivityType.objects.all()
    for activityType in activityTypes:
        if activityType.id == activity.ActivityType_id:
            activity.selected = 'selected'

    formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
    activity.ActivityDateTime = formatted_time
    print(vars(activityTypes))
    return render(request, 'manajerialactivity/update.html', {'activity': activity, 'activityTypes': activityTypes})


def delete(request, activity_id):
    try:
        activity = ManagerialActivity.objects.get(id=activity_id)
        activity.delete()

        return redirect(reverse('activity-list'))
    except ManagerialActivity.DoesNotExist:
        return redirect(reverse('activity-list'), {'error': "data tidak di temukan"})
    except Exception as e:
        return redirect(reverse('activity-list'), {'error': "Terjadi kesalahan saat operasi hapus"})


def update_status(request, activity_id):
    activity = ManagerialActivity.objects.get(id=activity_id)

    activity_types = ActivityType.objects.all()
    for activityType in activity_types:
        if activityType.id == activity.ActivityType_id:
            activity.selected = 'selected'

    count = ActivityApproval.objects.filter(UserId_id=request.user.id).filter(
        ActivityTypeId_id=activity.ActivityType_id).count()
    is_can_update_status = False
    if count > 0:
        is_can_update_status = True

    if request.method == 'POST' and is_can_update_status:
        activity.ActivityStatus = request.POST['activityStatus']
        activity.save()
        return redirect('activity-list')

    formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
    activity.ActivityDateTime = formatted_time
    return render(request, 'manajerialactivity/update_status.html',
                  {'activity': activity, 'activityTypes': activity_types, 'is_can_update_status': is_can_update_status})
