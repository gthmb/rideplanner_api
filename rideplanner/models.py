from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# from rest_framework.exceptions import ValidationError

class AccessSetting(models.Model):
    value = models.CharField(max_length=32)

    def __unicode__(self):
        return self.value


class UserPrivacySetting(models.Model):
    value = models.CharField(max_length=32)

    def __unicode__(self):
        return self.value


class UserGender(models.Model):
    value = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.value


class RideStateType(models.Model):
    value = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.value


class RideRouteType(models.Model):
    value = models.CharField(max_length=32)
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class RideRepeatType(models.Model):
    value = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.value


class RidePace(models.Model):
    name = models.CharField(max_length=32)
    value = models.IntegerField(max_length=2)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    age = models.IntegerField(max_length=2, null=True, blank=True)
    gender = models.ForeignKey(UserGender, null=True, blank=True)
    privacy_setting = models.ForeignKey(UserPrivacySetting, related_name="user_privacy_setting", default=1)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __unicode__(self):
        return self.user.get_username() + ' profile'


class Ride(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey('auth.User', related_name="creator")
    invitees = models.ManyToManyField('auth.User', related_name="ride_invitees", through="rideplanner.RideInvitation", null=True, blank=True)
    participants = models.ManyToManyField('auth.User', related_name="ride_participants", through="rideplanner.RideMembership", null=True, blank=True)
    ridergroups = models.ManyToManyField('rideplanner.RiderGroup', related_name="rider_groups", through="rideplanner.RiderGroupRideMembership", null=True, blank=True)
    editable_setting = models.ForeignKey(AccessSetting, related_name="ride_editable_setting", default=1)
    viewable_setting = models.ForeignKey(AccessSetting, related_name="ride_viewable_setting", default=1)
    state = models.ForeignKey(RideStateType, related_name="ride_state", default=1)
    route_type = models.ForeignKey(RideRouteType, related_name="ride_route", default=1)
    repeat = models.ForeignKey(RideRepeatType, related_name="ride_repeat", default=1)
    pace = models.ForeignKey(RidePace, related_name="ride_pace", default=1)

    class Meta:
        verbose_name = 'Ride'
        verbose_name_plural = 'Rides'

    def __unicode__(self):
        return self.name

class RideInvitation(models.Model):
    user = models.ForeignKey('auth.User')
    ride = models.ForeignKey('rideplanner.Ride')
    timestamp = models.DateTimeField(default=datetime.now)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'RideInvitation'
        verbose_name_plural = 'RideInvitations'

    def __unicode__(self):
        return self.user.get_username() + ' to ' + self.ride.name

class RideMembership(models.Model):
    user = models.ForeignKey('auth.User')
    ride = models.ForeignKey('rideplanner.Ride')
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'RideMembership'
        verbose_name_plural = 'RideMemberships'

    def __unicode__(self):
        return self.user.get_username() + ' to ' + self.ride.name

class RiderGroup(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey('auth.User', related_name="ridergroup_creator")
    description = models.CharField(max_length=255, null=True, blank=True)
    invitees = models.ManyToManyField('auth.User', related_name="ridergroup_invitees", through="rideplanner.RiderGroupInvitation", null=True, blank=True)
    participants = models.ManyToManyField('auth.User', related_name="ridergroup_participants", through="rideplanner.RiderGroupMembership", null=True, blank=True)
    viewable_setting = models.ForeignKey(AccessSetting, related_name="ridergroup_viewable_setting", default=1)
    editable_setting = models.ForeignKey(AccessSetting, related_name="ridergroup_editable_setting", default=1)  
    rides = models.ManyToManyField('rideplanner.Ride', related_name="rides", through="rideplanner.RiderGroupRideMembership", null=True, blank=True)

    class Meta:
        verbose_name = 'RiderGroup'
        verbose_name_plural = 'RiderGroups'

    def __unicode__(self):
        return self.name

class RiderGroupInvitation(models.Model):
    user = models.ForeignKey('auth.User')
    ridergroup = models.ForeignKey('rideplanner.RiderGroup')
    timestamp = models.DateTimeField(default=datetime.now)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'RiderGroupInvitation'
        verbose_name_plural = 'RiderGroupInvitations'

    def __unicode__(self):
        return self.user.get_username() + ' to ' + self.ridergroup.name

class RiderGroupMembership(models.Model):
    user = models.ForeignKey('auth.User')
    ridergroup = models.ForeignKey('rideplanner.RiderGroup')
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'RiderGroupMembership'
        verbose_name_plural = 'RiderGroupMemberships'

    def __unicode__(self):
        return self.user.get_username() + ' to ' + self.ridergroup.name

class RiderGroupRideMembership(models.Model):
    ride = models.ForeignKey('rideplanner.Ride')
    ridergroup = models.ForeignKey('rideplanner.RiderGroup')
    timestamp = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey('auth.User', related_name="ridergroupmembership_creator")

    class Meta:
        verbose_name = 'RiderGroupRide'
        verbose_name_plural = 'RiderGroupRides'

    def __unicode__(self):
        return self.ride.name + ' to ' + self.ridergroup.name
