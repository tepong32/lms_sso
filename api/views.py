from users.models import User, Profile
from django.contrib.auth.models import Group
from home.models import Leave, LeaveType, LeaveCounter
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, UserSerializer, ProfileSerializer
from .serializers import LeaveSerializer, LeaveTypeSerializer, LeaveCounterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "staff_id"

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('last_name')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leaves to be viewed or edited.
    """
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows LeavesTypes to be viewed or edited.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveCounterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows LeaveCounters to be viewed or edited.
    """
    queryset = LeaveCounter.objects.all()
    serializer_class = LeaveCounterSerializer
    permission_classes = [permissions.IsAuthenticated]