from django.contrib import admin

from rideplanner.models import (
	UserProfile,
	Ride,
	RideMembership,
	RideInvitation,
	RiderGroup,
	RiderGroupInvitation,
	RiderGroupMembership,
)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Ride)
admin.site.register(RideMembership)
admin.site.register(RideInvitation)
admin.site.register(RiderGroup)
admin.site.register(RiderGroupMembership)
admin.site.register(RiderGroupInvitation)