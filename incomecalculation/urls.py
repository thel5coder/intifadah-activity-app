from django.shortcuts import redirect
from django.urls import path, include
from django.shortcuts import redirect
from incomecalculation.templates.incomesetting import view as income_setting_view

urlpatterns = [
    path('setting/', income_setting_view.index, name='incomesetting-view'),
    path('setting/create', income_setting_view.create, name='incomesetting-create'),
    path('setting/update/<int:income_setting_id>', income_setting_view.update, name='incomesetting-update'),
    path('setting/delete/<int:income_setting_id>', income_setting_view.delete, name='incomesetting-delete'),
    path('setting/<int:income_setting_id>', income_setting_view.read, name='incomesetting-read'),
]
