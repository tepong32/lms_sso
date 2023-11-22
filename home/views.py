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
from .forms import LeaveForm, LeaveCounterForm


def homeView(request):
    user = User
    profile = Profile
    context = {
        'advisors': Profile.objects.filter(emp_type__name=EmployeeType.Type.ADVISOR),
        'tls': Profile.objects.filter(emp_type__name=EmployeeType.Type.TEAM_LEADER),
        'oms': Profile.objects.filter(emp_type__name=EmployeeType.Type.OPERATIONS_MGR),
        # 'adv_leaves': LeaveCounter.objects.filter(employee=user),
        'adv_all_leaves': LeaveCounter.objects.all()
    }
    return render(request, 'home/authed/home.html', context)



class ApplyLeaveView(LoginRequiredMixin, CreateView):       
    model = Leave
    form_class = LeaveForm
    second_form_class = LeaveCounterForm  # using a second form
    template_name = 'home/authed/apply_leave_form.html'
    success_message = "Leave request submitted."
    success_url = '/'

    def get_context_data(self, **kwargs):
        ### overriding get_context_data() to include two forms (for class-based views)
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['second_form'] = self.second_form_class(self.request.POST)
        else:
            data['second_form'] = self.second_form_class()
        return data

    def form_valid(self, form):
        form.instance.employee = self.request.user    # to automatically get the id of the current logged-in user
        context = self.get_context_data()
        second_form = context['second_form']
        if second_form.is_valid():
            self.object = form.save()
            second_form.instance = self.object
            second_form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        second_form = self.get_context_data()['second_form']
        if form.is_valid() and second_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    

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









'''

filter/query for leave counter only for the loggd-in user:
    'adv_leaves': LeaveCounter.objects.filter(employee=user)


'''