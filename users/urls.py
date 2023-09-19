from django.urls import path, include
from .views import *


### complete this some other time ###
urlpatterns = [
    path('', UsersIndex.as_view(), name='users index'),

]