from django import forms
from django.core.exceptions import ValidationError
from .models import Leave, LeaveCounter

class LeaveForm(forms.ModelForm):
    '''
        This form validates if the user can still apply for Leaves and raises errors if they've already used-up
        or is about to exceed the allowed_instances per quarter or per year.
    '''
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if employee and start_date and end_date:
            leave_counter = LeaveCounter.objects.get(employee=employee)
            leave_duration = (end_date - start_date).days + 1

            if leave_counter.instances_used_this_year + leave_duration > leave_counter.total_instances_per_year:
                raise ValidationError("You have reached or are about to exceed the allowed instances per year. /nPlease coordinate with your immediate supervisor if you need adjustments.")

            if leave_counter.instances_used_this_quarter + leave_duration > leave_counter.total_approved_per_quarter:
                raise ValidationError("You have reached or are about to exceed the allowed instances per quarter. /nPlease coordinate with your immediate supervisor if you need adjustments.")

        return cleaned_data


class LeaveCounterForm(forms.ModelForm):
    class Meta:
        model = LeaveCounter
        fields = ['total_instances_per_year', 'total_approved_per_quarter', 'additional_instances']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.profile.emp_type.name != EmployeeType.Type.TEAM_LEADER:
            self.fields['additional_instances'].disabled = True
