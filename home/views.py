from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from users.models import User, Profile, EmployeeType
from .models import Leave, LeaveCounter

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    )
from .forms import LeaveForm


def homeView(request):
    '''
        Currently listing all possible APIs here.
        Will need to separate them thru views after confirming they all work as intended.
    '''
    user = User # for listing all the users
    loggedin_user = request.user # for accessing the currently logged-in user's leave instances
    profile = Profile

    # initializing instances variables
    instances_used_this_year = None
    instances_used_this_quarter = None
    leave_counter = None

    if loggedin_user.is_authenticated:
        try:
            leave_counter = LeaveCounter.objects.get(employee=loggedin_user)
            instances_used_this_year = leave_counter.instances_used_this_year
            instances_used_this_quarter = leave_counter.instances_used_this_quarter
        except LeaveCounter.DoesNotExist:
            pass  # leave_counter does not exist for this user

    context = {
        'advisors': Profile.objects.filter(emp_type__name=EmployeeType.Type.ADVISOR),
        'tls': Profile.objects.filter(emp_type__name=EmployeeType.Type.TEAM_LEADER),
        'oms': Profile.objects.filter(emp_type__name=EmployeeType.Type.OPERATIONS_MGR),
        'adv_all_leaves': LeaveCounter.objects.all(),

        ### will return leave_counter.instances_used_this_year if leave_counter is not None, and 0 otherwise.
        'instances_used_this_year': getattr(leave_counter, 'instances_used_this_year', 0),
        ### will return leave_counter.instances_used_this_quarter if leave_counter is not None, and 0 otherwise.
        'instances_used_this_quarter': getattr(leave_counter, 'instances_used_this_quarter', 0),
    }
    return render(request, 'home/authed/home.html', context)



class ApplyLeaveView(LoginRequiredMixin, CreateView):       
    model = Leave
    form_class = LeaveForm
    template_name = 'home/authed/apply_leave_form.html'
    success_message = "Leave request submitted."
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'employee': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        '''
            The get_context_data method is used to add additional context variables to the template.
            If you’re using the leave_counter variable in your template, then you should keep this method.
            This method ensures that a LeaveCounter object is created for every user when they access the view.
        '''
        data = super().get_context_data(**kwargs)
        leave_counter, _ = LeaveCounter.objects.get_or_create(employee=self.request.user)
        data['leave_counter'] = leave_counter
        return data

    def form_valid(self, form):
        form.instance.employee = self.request.user    # to automatically get the id of the current logged-in user
        return super().form_valid(form)

    

class LeaveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Leave 
    form_class = LeaveForm
    template_name = 'home/authed/update_leave_form.html'
    success_message = "Leave application updated."
    success_url = '/'

    def form_valid(self, form):         
        form.instance.employee = self.request.user
        return super().form_valid(form)

    def test_func(self):
        leave = self.get_object()

        if self.request.user == leave.employee:
            return True
        return False


class LeaveDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):      
    model = Leave
    template_name = 'home/authed/delete_leave_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)

    def test_func(self):
        leave = self.get_object()

        if self.request.user == leave.employee:
            return True
        return False      



from .forms import IncreaseMaxInstancesForm
from .utils import increase_max_instances

def increase_max_instances_view(request):
    if request.method == 'POST':
        form = IncreaseMaxInstancesForm(request.POST)
        if form.is_valid():
            additional_instances = form.cleaned_data.get('additional_instances')
            increase_max_instances(additional_instances)
    else:
        form = IncreaseMaxInstancesForm()
    return render(request, 'home/authed/increase_max_instances.html', {'form': form})


# views.py
from django.views.generic.edit import FormView
from .forms import IncreaseMaxInstancesForm
from .utils import increase_max_instances
from django.contrib import messages

class IncreaseMaxInstancesView(FormView):
    template_name = 'home/authed/increase_max_instances.html'
    form_class = IncreaseMaxInstancesForm
    success_url = '/'  # replace with your success url

    def form_valid(self, form):
        additional_instances = form.cleaned_data.get('additional_instances')
        increase_max_instances(additional_instances)
        messages.success(self.request, f'Successfully increased max instances by {additional_instances} for all users.')
        return super().form_valid(form)