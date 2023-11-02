from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	'''
		these fields take arguments (required=true/false).
		by default, required=true
	'''
	# add fields to this form
	email = forms.EmailField() 

	class Meta:
		model = User 	# the mode that is going to be affected is the User model
		fields = ["staff_id", "email", "password1", "password2", ]


# after adding these forms, add it to the views.py
class UserUpdateForm(forms.ModelForm):
	'''
		these fields take arguments (required=true/false).
		by default, required=true
	'''
	email = forms.EmailField()

	class Meta:
		model = User 	# the model that is going to be affected is the User model, 
		fields = ["email"]	# hence its attributes are the ones in this "fields" variable // "username" field removed


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile 	# the model that is going to be affected by this form is the Profile model,
		fields = ["first_name", "middle_name", "last_name", "ext_name", "department", "image",]

