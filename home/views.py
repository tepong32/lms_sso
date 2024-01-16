from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


from users.models import User
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

from django.http import HttpResponse
from datetime import datetime


def homeView(request):
    '''
        Currently listing all possible APIs here.
        Will need to separate them thru views after confirming they all work as intended.
    '''
    user = User # for listing all the users
    loggedin_user = request.user # for accessing the currently logged-in user's leave instances

    ### displaying server time
    current_time = datetime.now()

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

        'advisors': user.objects.filter(is_advisor=True),
        'tls': user.objects.filter(is_team_leader=True),
        'oms': user.objects.filter(is_operations_manager=True),
        'adv_all_leaves': LeaveCounter.objects.all(),

        ### will return leave_counter.instances_used_this_year if leave_counter is not None, and 0 otherwise.
        'instances_used_this_year': getattr(leave_counter, 'instances_used_this_year', 0),
        ### will return leave_counter.instances_used_this_quarter if leave_counter is not None, and 0 otherwise.
        'instances_used_this_quarter': getattr(leave_counter, 'instances_used_this_quarter', 0),

        'leaves': Leave.objects.all(),

        'server_time': current_time
    }
    return render(request, 'home/authed/home.html', context) ### change this to a "base" page that separates view (thru include) for authed vs unauthed users
    ### this works for now as we just need to have the data/info displayed



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


# views.py
from django.views.generic.edit import FormView
from .forms import IncreaseMaxInstancesForm
from .utils import increase_max_instances
from django.contrib import messages


class IncreaseMaxInstancesView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'home/authed/increase_max_instances.html'
    form_class = IncreaseMaxInstancesForm
    success_url = '/'  # replace with your success url

    # def test_func(self):
    #     return self.request.user.is_staff or self.request.user.profile.emp_type == "Team Leader" or self.request.user.profile.emp_type == "Operations Mgr"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_team_leader or self.request.user.is_operations_manager

    def form_valid(self, form):
        year_additional_instances = form.cleaned_data.get('year_additional_instances')
        quarter_additional_instances = form.cleaned_data.get('quarter_additional_instances')
        increase_max_instances(year_additional_instances, quarter_additional_instances)
        messages.success(self.request, f'Successfully adjusted max instances for all users by: \nYearly: {year_additional_instances} \nQuarterly: {quarter_additional_instances}')
        return super().form_valid(form)


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def check_reset_date(request):
    if request.method == 'POST':
        leave_counter = LeaveCounter.objects.get(employee=request.user)
        leave_counter.reset_counters()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:  # GET request
        return render(request, 'home/authed/reset_counters.html')
