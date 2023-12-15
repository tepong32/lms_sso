from users.models import User, Profile
from django.contrib.auth.models import Group

from home.models import Leave, LeaveType, LeaveCounter
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'staff_id', 'email']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    ### adding the attr of the User class to ProfileSerializer (un-editable)
    ### then add it to the class Meta: below
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        ### removed emp_type and workgroup as they do not have their own serializers yet
        ### should I include them here or leave them as is?
        fields = ['url', 'user', 'first_name', 'middle_name', 'last_name', 'ext_name', 'image']


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
