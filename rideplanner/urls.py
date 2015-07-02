from django.conf.urls import url, include
from rideplanner import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False) # since Angular's ng-resource does some very stupid things with trailing slashes
router.register(r'users', views.UserViewSet)
router.register(r'user_profiles', views.UserProfileViewSet)
router.register(r'rides', views.RideViewSet)
router.register(r'ride_memberships', views.RideMembershipViewSet)
router.register(r'ride_invitations', views.RideInvitationViewSet)
router.register(r'ridergroup', views.RiderGroupViewSet)
router.register(r'ridergroup_memberships', views.RiderGroupMembershipViewSet)
router.register(r'ridergroup_invitations', views.RiderGroupInvitationViewSet)
router.register(r'ridergroup_ride_memberships', views.RiderGroupRideMembershipViewSet)
router.register(r'rider_license', views.RiderLicenseViewSet)
router.register(r'rider_license_type', views.RiderLicenseTypeViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^rides/(?P<pk>[0-9]+)/participants/(?P<upk>[0-9]+)$', views.ride_membership_shortcut),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]