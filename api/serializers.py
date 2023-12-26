from users.models import User
from django.contrib.auth.models import Group

from home.models import Leave, LeaveType, LeaveCounter
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'staff_id', 'email', 'first_name', 'middle_name', 'last_name', 'ext_name', 'image']
        field = "__all__"

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class LeaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"

class LeaveTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"

class LeaveCounterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LeaveCounter
        fields = "__all__"
