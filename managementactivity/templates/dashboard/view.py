from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from managementactivity.models import ManagerialActivity, ActivityType
from datetime import datetime
from managementactivity.utils import ActivityStatus
import time


@login_required(login_url='/login/')
def dashboard(request):
    date_now = datetime.now().date()
    activities = ManagerialActivity.objects.filter(ManagerialUser_id=request.user.id)
    countActivityManagerialToday = 0
    countRejectedActivityToday = 0
    countApprovedActivityToday = 0
    countWaitingApprovalActivityToday = 0
    for activity in activities:
        activity_date_time = datetime.fromtimestamp(activity.ActivityDateTime)
        activity_date = activity_date_time.date()
        print("activity_date_time")
        print()
        print("date now")
        print(date_now.timetuple())
        if activity_date.timetuple().tm_mon == date_now.timetuple().tm_mon:
            countActivityManagerialToday += 1
            if activity.ActivityStatus == ActivityStatus.REJECTED:
                countRejectedActivityToday += 1
            if activity.ActivityStatus == ActivityStatus.APPROVED:
                countApprovedActivityToday += 1
            if activity.ActivityStatus == ActivityStatus.WAITING_APPROVAL:
                countWaitingApprovalActivityToday += 1

    return render(request, 'dashboard/dashboard.html', {"count_activity_today": countActivityManagerialToday,
                                                        "count_rejected": countRejectedActivityToday,
                                                        "count_approved": countApprovedActivityToday,
                                                        "count_waiting_approval": countWaitingApprovalActivityToday,
                                                        "approved": ActivityStatus.APPROVED,
                                                        "rejected": ActivityStatus.REJECTED,
                                                        "waiting_approval": ActivityStatus.WAITING_APPROVAL})
