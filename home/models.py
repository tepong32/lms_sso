from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User, EmployeeType, Profile





class LeaveType(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')

    def __str__(self):
        return self.name

class Leave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Employee', related_name="leave_filer")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, verbose_name='Leave Type')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'approved':
            # Update LeaveCounter only when leave is approved
            leave_counter, _ = LeaveCounter.objects.get_or_create(employee=self.employee)
            leave_duration = self.end_date - self.start_date + timedelta(days=1) # Include both start and end dates
            leave_counter.instances_used_this_year += leave_duration.days
            leave_counter.instances_used_this_quarter += leave_duration.days
            leave_counter.save()

class LeaveCounter(models.Model):
    '''
        This counts and limits the approved leaves of each user.
        We may need to change the values used as hours instead of # of days to incorporate accrueable leave credits
    '''
    employee = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Employee')
    total_instances_per_year = models.PositiveIntegerField(default=25, verbose_name='Total Instances Per Year')
    total_approved_per_quarter = models.PositiveIntegerField(default=6, verbose_name='Total Approved Per Quarter')
    instances_used_this_year = models.PositiveIntegerField(default=0, verbose_name='Instances Used This Year')
    instances_used_this_quarter = models.PositiveIntegerField(default=0, verbose_name='Instances Used This Quarter')
    last_year_reset_date = models.DateField(null=True, blank=True, verbose_name='Last Year Reset Date')
    last_quarter_reset_date = models.DateField(null=True, blank=True, verbose_name='Last Quarter Reset Date')
    additional_instances = models.PositiveIntegerField(default=0, verbose_name='Additional Instances')



    import calendar

    def reset_counters(self):
        '''
        reset_counters method will reset the counters if the last reset date is less than the first day of the current quarter.
        current quarter is determined by calculating the quarter index based on the current month.
        '''
        now = timezone.localtime(timezone.now())
        current_year = now.year
        current_quarter = (now.month - 1) // 3 + 1
        quarter_start_month = (current_quarter - 1) * 3 + 1
        quarter_start_date = now.replace(month=quarter_start_month, day=1)

        if self.last_year_reset_date is None or self.last_year_reset_date < quarter_start_date:
            self.instances_used_this_year = 0
            self.last_year_reset_date = quarter_start_date

        if self.last_quarter_reset_date is None or self.last_quarter_reset_date < quarter_start_date:
            self.instances_used_this_quarter = 0
            self.last_quarter_reset_date = quarter_start_date

        self.save()

    ### properties added to consider additional_instances of Leaves (admin-editable only)
    @property
    def total_allowed_per_year(self):
        return self.total_instances_per_year + self.additional_instances

    @property
    def total_allowed_per_quarter(self):
        return self.total_approved_per_quarter + self.additional_instances