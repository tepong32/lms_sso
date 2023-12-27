# this file is so that newly-registered users can have the "defaults" saved in their profiles.
from django.db.models.signals import post_save	# a signal that gets fired whenever an object is saved
from .models import User#, Profile, EmployeeType, WorkGroup	# User is the sender of the signal
from django.dispatch import receiver 	# receiver




# @receiver(post_save, sender=User)	# (arguments == the_signal, sender)
# def create_profile(sender, instance, created, **kwargs):
# 	'''
# 		a function to automatically create a profile for every time a new user registers/ is created
# 	'''
# 	if created:
# 		advisor_type = EmployeeType.objects.get(name=EmployeeType.Type.ADVISOR)
# 		us_workgroup = WorkGroup.objects.get(name=WorkGroup.Type.US)
# 		Profile.objects.create(user=instance, emp_type=advisor_type, workgroup=us_workgroup)

# @receiver(post_save, sender=User)	# (arguments == the_signal, sender)
# def save_profile(sender, instance, **kwargs):
# 	'''
# 		a function to save the profile
# 	'''
# 	instance.profile.save()

# '''
# 	after creation of this file, we must save the signals to the app's app.py (users/apps.py)
# '''


# I wont be needing the signals, I guess?