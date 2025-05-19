from calendar import month

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from managementactivity.models import ManagerialActivity, ActivityType, ActivityApproval
from datetime import datetime
from managementactivity.utils import ActivityStatus,DateTimeHelper
import time


@login_required(login_url='/login/')
def dashboard(request):
    date_now = datetime.now().date()
    activities = ManagerialActivity.objects.filter(ManagerialUser_id=request.user.id).with_month('ActivityDateTime').filter(
        month=DateTimeHelper.get_current_local_time().month)
    countActivityManagerialToday = 0
    countApprovedActivityToday = 0
    countWaitingApprovalActivityToday = 0

    approvals = ActivityApproval.objects.filter(UserId_id=request.user.id)
    activity_type_ids = []
    for approval in approvals:
        activity_type_ids.append(approval.ActivityTypeId_id)

    print(activity_type_ids)

    count_need_approvals = ManagerialActivity.objects.with_month('ActivityDateTime').filter(
        month=DateTimeHelper.get_current_local_time().month).filter(ActivityType_id__in=activity_type_ids).filter(
        ActivityStatus=ActivityStatus.WAITING_APPROVAL).exclude(ManagerialUser_id=request.user.id).count()

    for activity in activities:
        activity_date_time = datetime.fromtimestamp(activity.ActivityDateTime)
        activity_date = activity_date_time.date()
        if activity_date.timetuple().tm_mon == date_now.timetuple().tm_mon:
            countActivityManagerialToday += 1
            if activity.ActivityStatus == ActivityStatus.APPROVED:
                countApprovedActivityToday += 1
            if activity.ActivityStatus == ActivityStatus.WAITING_APPROVAL:
                countWaitingApprovalActivityToday += 1

    return render(request, 'dashboard/dashboard.html', {"count_activity_today": countActivityManagerialToday,
                                                        "count_approved": countApprovedActivityToday,
                                                        "count_waiting_approval": countWaitingApprovalActivityToday,
                                                        "approved": ActivityStatus.APPROVED,
                                                        "rejected": ActivityStatus.REJECTED,
                                                        "waiting_approval": ActivityStatus.WAITING_APPROVAL,
                                                        "count_needs_approval": count_need_approvals})
