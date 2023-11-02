from django.shortcuts import render
from users.models import User
# Create your views here.

def homeView(request):
    user = User
    context = {}
    return render(request, 'home/authed/home.html', context)