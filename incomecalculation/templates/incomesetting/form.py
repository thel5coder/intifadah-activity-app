from random import choices

from incomecalculation.baseform import BootstrapForm
from django import forms


class IncomeSettingForm(BootstrapForm):
    option = [
        ('FIX','Fix'),
        ('PERSENTASE','Persentase'),
    ]
    key = forms.CharField(label='Key', widget=forms.TextInput, required=True)
    value = forms.CharField(label='Value', widget=forms.TextInput, required=True)
    type = forms.ChoiceField(label='Type', widget=forms.Select, choices=option, required=True)
