from django import forms
from django.forms import CheckboxInput

class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add 'form-control' to all fields except checkboxes
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control form-user'
            # # Add 'is-invalid' if the field has errors (after validation)
            # if self.errors.get(field_name):
            #     field.widget.attrs['class'] += ' is-invalid'

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'