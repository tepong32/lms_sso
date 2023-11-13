from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User

class LeaveType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Leave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'approved':
            # Update LeaveCounter only when leave is approved
            leave_counter, _ = LeaveCounter.objects.get_or_create(employee=self.employee)
            leave_duration = self.end_date - self.start_date + timedelta(days=1)  # Include both start and end dates
            leave_counter.instances_used_this_year += leave_duration.days
            leave_counter.instances_used_this_quarter += leave_duration.days
            leave_counter.save()

class LeaveCounter(models.Model):
    '''
        This counts and limits the approved leaves of each user.
        We may need to change the values used as hours instead of # of days to incorporate accrueable leave credits
    '''
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    total_instances_per_year = models.PositiveIntegerField(default=25)
    total_approved_per_quarter = models.PositiveIntegerField(default=6)
    instances_used_this_year = models.PositiveIntegerField(default=0)
    instances_used_this_quarter = models.PositiveIntegerField(default=0)
    last_year_reset_date = models.DateField(null=True, blank=True)
    last_quarter_reset_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - Leave Counter"

    def reset_counters(self):
        today = timezone.now().date()
        if not self.last_year_reset_date or self.last_year_reset_date.year < today.year:
            # Reset yearly counters on January 1st
            self.instances_used_this_year = 0
            self.last_year_reset_date = today
        if not self.last_quarter_reset_date or self.last_quarter_reset_date < today:
            # Reset quarterly counters on January, April, July, and October
            if today.month in [1, 4, 7, 10]:
                self.instances_used_this_quarter = 0
                self.last_quarter_reset_date = today
        self.save()
