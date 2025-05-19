from django.shortcuts import render, redirect
from managementactivity.models import ManagerialActivity, ActivityType
from managementactivity.utils import ActivityStatus, DateTimeHelper
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from managementactivity.models import ActivityApproval
from django.contrib.auth.models import User
from django.db.models import DateTimeField, Q
from django.db.models.functions import Cast


def index(request):
    query = ManagerialActivity.objects.all()
    query = query.with_month('ActivityDateTime').filter(
        month=DateTimeHelper.get_current_local_time().month)

    if request.GET.get('status'):
        query = query.filter(ActivityStatus=request.GET.get('status'))

    if request.GET.get('type'):
        query = query.filter(ActivityType_id=request.GET.get('type'))

    exclude = request.GET.get('exclude')
    if exclude == "1":
        query = query.exclude(ManagerialUser_id=request.user.id)
    else:
        query = query.filter(ManagerialUser_id=request.user.id)

    activities = query.order_by('-ActivityDateTime')

    activity_approvals = ActivityApproval.objects.filter(UserId_id=request.user.id)
    approval_ids = []
    for approval in activity_approvals:
        approval_ids.append(approval.ActivityTypeId_id)

    print(approval_ids)

    for activity in activities:
        activity.status = {'value': ActivityStatus.get_key_text(activity.ActivityStatus),
                           'badge': ActivityStatus.get_badge_status(activity.ActivityStatus)}
        formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
        activity.ActivityDateTime = formatted_time

    return render(request, 'manajerialactivity/list.html', {'activities': activities,'approval_ids': approval_ids})


def all_activity(request):
    activities = ManagerialActivity.objects.all()
    for activity in activities:
        activity.status = {'value': ActivityStatus.get_key_text(activity.ActivityStatus),
                           'badge': ActivityStatus.get_badge_status(activity.ActivityStatus)}
        formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
        activity.ActivityDateTime = formatted_time
        activity.userManagerial = User.objects.filter(id=activity.ManagerialUser_id).first()

    return render(request, 'manajerialactivity/all.html', {'activities': activities})


def create(request):
    if request.method == 'POST':
        activity = ManagerialActivity()
        if 'activityImage' in request.FILES:
            activity.ActivityImage = request.FILES['activityImage']
        else:
            activity.ActivityImage = 'blank.png'
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
        if 'activityImage' in request.FILES:
            activity.ActivityImage = request.FILES['activityImage']
        else:
            activity.ActivityImage = 'blank.png'
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

    if request.method == 'POST':
        count = ActivityApproval.objects.filter(UserId_id=request.user.id).filter(
            ActivityTypeId_id=activity.ActivityType_id).count()
        is_can_update_status = False
        error = {"is_error": True, "message": "Anda tidak punya hak akses untuk merubah status"}
        if count > 0:
            is_can_update_status = True

        if is_can_update_status:
            status = ActivityStatus.WAITING_APPROVAL
            if request.POST['activityScore'] != 0:
                status = ActivityStatus.APPROVED

            activity.ActivityStatus = status
            activity.RejectedReason = ""
            activity.ActivityScore = request.POST['activityScore']
            activity.save()
            error["is_error"] = False
            error["message"] = ""

        return redirect(reverse('activity-list'), {'error': error})

    formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
    activity.ActivityDateTime = formatted_time
    return render(request, 'manajerialactivity/update_status.html',
                  {'activity': activity, 'activityTypes': activity_types})


def activity_statistics(request):
    return render(request, 'manajerialactivity/statistics.html')


def activity_by_status(request, activity_status):
    approvals = ActivityApproval.objects.filter(UserId_id=request.user.id)
    activity_type_ids = []
    for approval in approvals:
        activity_type_ids.append(approval.ActivityTypeId_id)

    activities = ManagerialActivity.objects.with_month('ActivityDateTime').filter(
        month=DateTimeHelper.get_current_local_time().month).filter(ActivityType_id__in=activity_type_ids)

    for activity in activities:
        activity.status = {'value': ActivityStatus.get_key_text(activity.ActivityStatus),
                           'badge': ActivityStatus.get_badge_status(activity.ActivityStatus)}
        formatted_time = datetime.fromtimestamp(activity.ActivityDateTime).strftime('%d-%m-%Y %H:%M')
        activity.ActivityDateTime = formatted_time

    return render(request, 'manajerialactivity/activity_by_status.html', {'activities': activities})


def activity_type_list(request):
    activities = ManagerialActivity.objects.with_month('ActivityDateTime').filter(
        month=DateTimeHelper.get_current_local_time().month).exclude(ManagerialUser_id=request.user.id)

    activity_types = ActivityType.objects.all().order_by('id')
    count = {}
    for activity in activities:
        for activity_type in activity_types:
            if not hasattr(activity_type,'count'):
                setattr(activity_type,'count',0)

            if activity_type.id == activity.ActivityType_id:
                activity_type.count += 1

    return render(request, 'manajerialactivity/activity_type_list.html',
                  {'count': count, 'activity_types': activity_types})


def activity_need_approval(request):
    approvals = ActivityApproval.objects.filter(UserId_id=request.user.id)
    activity_type_ids = []
    for approval in approvals:
        activity_type_ids.append(approval.ActivityTypeId_id)

    activities = ManagerialActivity.objects.with_month('ActivityDateTime').filter(
        month=DateTimeHelper.get_current_local_time().month).filter(ActivityType_id__in=activity_type_ids).filter(
        ActivityStatus=ActivityStatus.WAITING_APPROVAL).exclude(ManagerialUser_id=request.user.id)

    return render(request, 'manajerialactivity/activity_by_status.html', {'activities': activities, 'approval': True})
