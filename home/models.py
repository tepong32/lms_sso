from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User


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

    def auto_approve(self):
        # Get the WorkGroup of the employee
        workgroup = self.employee.workgroup

        # Get the number of leaves taken on the day the leave is filed
        leaves_taken = Leave.objects.filter(employee__workgroup=workgroup, start_date=self.start_date, status='approved').count()

        # If the number of leaves taken is less than the allowed leaves per day, set the status to 'approved'
        if leaves_taken < workgroup.allowed_leaves_per_day:
            self.status = 'approved'
            self.save()

    def save(self, *args, **kwargs):
        # Check if the status has changed to 'approved'
        if self.pk is not None:
            orig = Leave.objects.get(pk=self.pk)
            if orig.status != self.status and self.status == 'approved':
                # Update LeaveCounter only when leave is approved
                leave_counter, _ = LeaveCounter.objects.get_or_create(employee=self.employee)
                leave_duration = self.end_date - self.start_date + timedelta(days=1) # Include both start and end dates
                leave_counter.instances_used_this_year += leave_duration.days
                leave_counter.instances_used_this_quarter += leave_duration.days
                leave_counter.save()

        super().save(*args, **kwargs)

class LeaveCounter(models.Model):
    '''
        This counts and limits the approved leaves of each user.
        We may need to change the values used as hours instead of # of days to incorporate accrueable leave credits
    '''
    employee = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Requester')
    max_instances_per_year = models.PositiveIntegerField(default=25, verbose_name='Max. Instances Per Year', help_text="This count shows the default. Always check for 'additional_instances' for the actual computation of the max_allowed instances per_year and per_quarter.")
    max_instances_per_quarter = models.PositiveIntegerField(default=6, verbose_name='Max. Instances Per Quarter', help_text="This count shows the default. Always check for 'additional_instances' for the actual computation of the max_allowed instances per_year and per_quarter.")
    instances_used_this_year = models.PositiveIntegerField(default=0, verbose_name='Instances Used This Year')
    instances_used_this_quarter = models.PositiveIntegerField(default=0, verbose_name='Instances Used This Quarter')
    last_year_reset_date = models.DateField(null=True, blank=True, verbose_name='Last Year Reset Date')
    last_quarter_reset_date = models.DateField(null=True, blank=True, verbose_name='Last Quarter Reset Date')
    additional_instances_per_year = models.PositiveIntegerField(default=0, verbose_name='Additional Instances Per Year')
    additional_instances_per_quarter = models.PositiveIntegerField(default=0, verbose_name='Additional Instances Per Quarter')
    reset_this_quarter = models.BooleanField(default=False) # safety net to ensure that the reset will only be done once per quarter

    def save(self, *args, **kwargs):
        self.max_instances_per_year += self.additional_instances_per_year
        self.max_instances_per_quarter += self.additional_instances_per_quarter
        ### if we need to set the attributes to 0 again after adding counts to the max_instances, uncomment the 2 lines below
        self.additional_instances_per_year = 0
        self.additional_instances_per_quarter = 0

        if not self.reset_this_quarter:
            ### "If the reset_this_quarter==False, call the reset_counters()"
            self.reset_counters()
        super().save(*args, **kwargs)


    import calendar

    def carry_over(self):
        '''
        carry_over method will carry over the unused instances to the next quarter.
        current quarter is determined by calculating the quarter index based on the current month.
        '''
        now = timezone.localtime(timezone.now())
        current_quarter = (now.month - 1) // 3 + 1

        if self.last_quarter_reset_date is not None:
            last_quarter = (self.last_quarter_reset_date.month - 1) // 3 + 1
            if last_quarter < current_quarter or (last_quarter == 4 and current_quarter == 1):  # If a new quarter has started
                unused_instances = self.max_instances_per_quarter - self.instances_used_this_quarter
                self.max_instances_per_quarter += unused_instances
                self.instances_used_this_quarter = 0
                self.last_quarter_reset_date = now
                self.save()

    def reset_counters(self):
        '''
        reset_counters method will reset the counters if the last reset date is less than the first day of the current quarter.
        current quarter is determined by calculating the quarter index based on the current month.
        '''
        now = timezone.localtime(timezone.now())
        current_year = now.year
        current_quarter = (now.month - 1) // 3 + 1
        quarter_start_month = (current_quarter - 1) * 3 + 1
        quarter_start_date = now.replace(month=quarter_start_month, day=1).date() # converting quarter_start_date to datetime.date because "now.replace()" uses datetime.datetime"

        if self.last_year_reset_date is None or self.last_year_reset_date < quarter_start_date:
            self.instances_used_this_year = 0
            self.last_year_reset_date = quarter_start_date
            self.max_instances_per_year = self.max_instances_per_year
            self.additional_instances_per_quarter = 0

        if self.last_quarter_reset_date is None or self.last_quarter_reset_date < quarter_start_date:
            # Before resetting the instances_used_this_quarter, calculate the unused instances and add them to max_instances_per_quarter
            unused_instances = self.max_instances_per_quarter - self.instances_used_this_quarter
            self.max_instances_per_quarter = self.max_instances_per_quarter + unused_instances  # Reset max_instances_per_quarter to 6 plus any unused instances

            self.instances_used_this_quarter = 0
            self.last_quarter_reset_date = quarter_start_date
            self.additional_instances_per_quarter = 0
            self.reset_this_quarter = True ### setting this to true on save of this reset_counters() to make sure it'll only happen once per quarter
        self.save()

    ### properties added to consider additional_instances of Leaves (admin-editable only)
    @property
    def total_allowed_per_year(self):
        return self.max_instances_per_year + self.additional_instances_per_year

    @property
    def total_allowed_per_quarter(self):
        return self.max_instances_per_quarter + self.additional_instances_per_quarter

    def __str__(self):
        return f'Leave Counter for {str(self.employee)}'