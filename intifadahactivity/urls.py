"""
URL configuration for intifadahactivity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from managementactivity.templates.login import view
from managementactivity.templates.dashboard import view as dashboard
from managementactivity.templates.activitytype import view as activitytype
from managementactivity.templates.user import view as user
from managementactivity.templates.manajerialactivity import view as activity
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('login'), name='redirect-root'),
    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('login/', view.login_view, name='login'),
    path('logout/', view.logout_view, name='logout'),

    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('activity-type/', activitytype.index, name='activitytype'),
    path('activity-type/add', activitytype.create, name='activitytype-add'),
    path('user/', user.create, name='user-create'),

    path('activity/', activity.index, name='activity-list'),
    path('activity/all', activity.all_activity, name='activity-all'),
    path('activity/create', activity.create, name='activity-create'),
    path('activity/statistics', activity.activity_statistics, name='activity-statistics'),
    path('activity/activity-type', activity.activity_type_list, name='activity-type-list'),
    path('activity/need-approval',activity.activity_need_approval,name='activity-need-approval'),
    path('activity/<int:activity_status>', activity.activity_by_status, name='activity-by-status'),

    path("activity/status/<int:activity_id>", activity.update_status, name="activity-update-status"),
    path("activity/update/<int:activity_id>", activity.update, name='activity-update'),
    path("activity/delete/<int:activity_id>", activity.delete, name='activity-delete'),

    path('income/',include('incomecalculation.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
