from django.shortcuts import render
from users.models import User, Profile, EmployeeType
from .models import LeaveCounter
# Create your views here.

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



'''

filter/query for leave counter only for the loggd-in user:
    'adv_leaves': LeaveCounter.objects.filter(employee=user)


'''