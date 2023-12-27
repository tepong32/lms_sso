from django import forms
<<<<<<< HEAD
from .models import User, WorkGroup
=======
from .models import User#, WorkGroup
>>>>>>> master
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
	'''
		these fields take arguments (required=true/false).
		by default, required=true
	'''
	# add fields to this form
	email = forms.EmailField() # set here for validation purposes

	class Meta:
		model = User 	# the mode that is going to be affected is the User model
		fields = ["staff_id", "email", "password1", "password2", 'first_name', 'middle_name', 'last_name', 'ext_name', 'workgroup'] #


# after adding these forms, add it to the views.py
class UserUpdateForm(forms.ModelForm):
	'''
		these fields take arguments (required=true/false).
		by default, required=true
	'''
	email = forms.EmailField()

	class Meta:
		model = User 	# the model that is going to be affected is the User model, 
		fields = ["email", "first_name", "middle_name", "last_name", "ext_name"]	# "staff_id" field removed for it should not be changeable , 'workgroup'


class WorkGroupForm(forms.ModelForm):
    class Meta:
        model = WorkGroup
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == "Default":
            raise forms.ValidationError("You must select a workgroup.")
        return name

		fields = ["email", "first_name", "middle_name", "last_name", "ext_name", "workgroup"]	# "staff_id" field removed for it should not be changeable , 'workgroup'


# class WorkGroupForm(forms.ModelForm):
#     class Meta:
#         model = WorkGroup
#         fields = ['name']

#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if name == "Default":
#             raise forms.ValidationError("You must select a workgroup.")
#         return name

