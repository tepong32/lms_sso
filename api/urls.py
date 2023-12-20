from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.ProfileViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'leaves', views.LeaveViewSet)
router.register(r'leavetypes', views.LeaveTypeViewSet)
router.register(r'leavecounters', views.LeaveCounterViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls