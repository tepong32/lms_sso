from django.db.models.signals import post_save
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


from users.models import User

@receiver(post_save, sender=User)
def create_leave_counter(sender, instance, created, **kwargs):
    if created:
        print(f'User object: {instance}')
        leave_counter = LeaveCounter.objects.create(employee=instance)
        print(f'LeaveCounter object: {leave_counter}')

@receiver(post_save, sender=User)
def save_leave_counter(sender, instance, **kwargs):
    instance.leavecounter.save()