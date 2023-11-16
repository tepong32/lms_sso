from django.shortcuts import render
from users.models import User, Profile, EmployeeType
# Create your views here.

def homeView(request):
    user = User
    profile = Profile
    context = {
        'advisors': Profile.objects.filter(emp_type__name=EmployeeType.Type.ADVISOR),
        'tls': Profile.objects.filter(emp_type__name=EmployeeType.Type.TEAM_LEADER),
        'oms': Profile.objects.filter(emp_type__name=EmployeeType.Type.OPERATIONS_MGR),
    }
    return render(request, 'home/authed/home.html', context)