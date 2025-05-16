from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from managementactivity.models import ManagerialActivity, ActivityType
from datetime import datetime


@login_required(login_url='/login/')
def dashboard(request):
    # date_now = datetime.now().date()
    # activities = ManagerialActivity.objects.filter(MangerialUser_id=request.user.id)
    # countActivityManagerialToday = 0
    # countRejectedActivityToday = 0
    # countApprovedActivityToday = 0
    # countWaitingApprovalActivityToday = 0
    # for activity in activities:
    #     activityDateTime = datetime.datetime.fromtimestamp(activity.ActivityDateTime)
    #     activityDate = activityDateTime.date()
    #     if activityDate
    #     if activity.ActivityType == ActivityType.REJECTED:
    #         countRejectedActivityToday += 1
    #     if activity.ActivityType == ActivityType.APPROVED:
    #         countApprovedActivityToday += 1
    #     if activity.ActivityType == ActivityType.WAITING_APPROVAL:
    #         countWaitingApprovalActivityToday += 1


    return render(request, 'dashboard/dashboard.html')
