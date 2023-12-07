from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Leave, LeaveCounter
from django.utils import timezone


@receiver(post_save, sender=Leave)
def check_reset_dates(sender, instance, **kwargs):
    # Check if today's date matches reset dates
    '''
        This function automatically checks for certain dates to trigger the reset_counters() of the LeaveCounter model
        Do not forget to connect signal this to apps.py
    '''
    today = timezone.now().date()
    if today.month in [1, 4, 7, 10]:
        leave_counter, _ = LeaveCounter.objects.get_or_create(employee=instance.employee)
        leave_counter.reset_counters()


from datetime import timedelta

@receiver(post_save, sender=Leave)
def create_or_update_leave_counter(sender, instance, created, **kwargs):
    leave_counter = LeaveCounter.objects.get(employee=instance.employee)
    leave_duration = (instance.end_date - instance.start_date).days + 1 # Include both start and end dates
    if created:
        leave_counter.instances_used_this_year += leave_duration.days
        leave_counter.instances_used_this_quarter += leave_duration.days
    else:
        original_leave = sender.objects.get(pk=instance.pk)
        original_duration = (original_leave.end_date - original_leave.start_date).days + 1
        leave_counter.instances_used_this_year += leave_duration - original_duration
        leave_counter.instances_used_this_quarter += leave_duration - original_duration
    leave_counter.save()

@receiver(post_delete, sender=Leave)
def delete_leave_counter(sender, instance, **kwargs):
    leave_counter = LeaveCounter.objects.get(employee=instance.employee)
    leave_duration = (instance.end_date - instance.start_date).days + 1 # Include both start and end dates
    leave_counter.instances_used_this_year -= leave_duration.days
    leave_counter.instances_used_this_quarter -= leave_duration.days
    leave_counter.save()
