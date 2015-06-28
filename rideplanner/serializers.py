# from django.forms import widgets
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ObjectDoesNotExist

from rideplanner.models import (
    Ride, 
    UserProfile, 
    UserGender,
    RideMembership, 
    RideInvitation,
    AccessSetting,
    RideStateType,
    RideRouteType,
    RideRepeatType,
    RidePace,
    RiderGroup,
    RiderGroupInvitation,
    RiderGroupMembership,
    RiderGroupRideMembership
)

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        
        # create User and hash the PW
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        # create a UserProfile and associate it with this user
        profile = UserProfile()
        profile.user = user;
        profile.save();

        # need to create a API token too
        token = Token.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ('id', 'password', 'first_name', 'last_name', 'email', 'username', 'url', )
        write_only_fields = ('password',)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    gender = serializers.SlugRelatedField(slug_field='value', queryset=UserGender.objects.all())
    
    class Meta:
        model = UserProfile
        fields = ('user', 'age', 'url', 'gender')


class RideStateTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RideStateType
        fields = ('id', 'value',)


class RideRouteTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RideRouteType
        fields = ('id', 'value', 'name')
        read_only_fields = ('value',)


class RideRepeatTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RideRepeatType
        fields = ('id', 'value',)

class RidePaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RidePace
        fields = ('id', 'name', 'value')
        read_only_fields = ('value',)

class RideGroupForRideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RiderGroup
        fields = ('id', 'name', 'description', 'url')

class RideForRiderGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ride
        fields = ('id', 'name', 'url')

class RideSerializer(serializers.HyperlinkedModelSerializer):
    creator = UserSerializer(read_only=True)
    participants = UserSerializer(read_only=True, many=True)
    invitees = UserSerializer(read_only=True, many=True)
    ridergroups = RideGroupForRideSerializer(read_only=True, many=True)
    editable_setting = serializers.SlugRelatedField(slug_field='value', queryset=AccessSetting.objects.all())
    viewable_setting = serializers.SlugRelatedField(slug_field='value', queryset=AccessSetting.objects.all())
    state = serializers.SlugRelatedField(slug_field='value', queryset=RideStateType.objects.all())
    repeat = serializers.SlugRelatedField(slug_field='value', queryset=RideRepeatType.objects.all())
    route_type = serializers.SlugRelatedField(slug_field='value', queryset=RideRouteType.objects.all())
    pace = serializers.SlugRelatedField(slug_field='name', queryset=RidePace.objects.all())
    
    class Meta:
        model = Ride
        fields = ('id', 'name', 'creator', 'participants', 'invitees', 'ridergroups', 'url', 'editable_setting', 'viewable_setting', 'state', 'repeat', 'route_type', 'pace')


class RideMembershipSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="user-detail", queryset=User.objects.all())
    ride = serializers.HyperlinkedRelatedField(view_name="ride-detail", queryset=Ride.objects.all())

    def create(self, validated_data):
        if( RideMembership.objects.filter(user=validated_data['user'], ride=validated_data['ride']).exists() ):
            raise ValidationError('User [%s] is already in Ride [%s]' % (validated_data['user'], validated_data['ride']))

        membership = super(RideMembershipSerializer, self).create(validated_data)

        return membership

    class Meta:
        model = RideMembership
        fields = ('id', 'timestamp', 'ride', 'user', 'url',)
        read_only_fields = ('timestamp',)


class RideInvitationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="user-detail", queryset=User.objects.all())
    ride = serializers.HyperlinkedRelatedField(view_name="ride-detail", queryset=Ride.objects.all())
    accepted = serializers.BooleanField(required=False)

    def create(self, validated_data):
        if(RideInvitation.objects.filter(user=validated_data['user'], ride=validated_data['ride']).exists()):
            raise ValidationError('User [%s] is already invited to Ride [%s]' % (validated_data['user'], validated_data['ride']))
        
        invitation = super(RideInvitationSerializer, self).create(validated_data)

        return invitation

    class Meta:
        model = RideInvitation
        fields = ('id', 'timestamp', 'ride', 'user', 'accepted', 'url',)
        read_only_fields = ('timestamp',)

class RiderGroupSerializer(serializers.HyperlinkedModelSerializer):
    creator = UserSerializer(read_only=True)
    participants = UserSerializer(read_only=True, many=True)
    invitees = UserSerializer(read_only=True, many=True)
    rides = RideForRiderGroupSerializer(read_only=True, many=True)
    editable_setting = serializers.SlugRelatedField(slug_field='value', queryset=AccessSetting.objects.all())
    viewable_setting = serializers.SlugRelatedField(slug_field='value', queryset=AccessSetting.objects.all())

    class Meta:
        model = RiderGroup
        fields = ('id', 'name', 'description', 'creator', 'participants', 'invitees', 'url', 'viewable_setting', 'editable_setting', 'rides')


class RiderGroupMembershipSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="user-detail", queryset=User.objects.all())
    ridergroup = serializers.HyperlinkedRelatedField(view_name="ridergroup-detail", queryset=RiderGroup.objects.all())

    def create(self, validated_data):
        if( RiderGroupMembership.objects.filter(user=validated_data['user'], ridergroup=validated_data['ridergroup']).exists() ):
            raise ValidationError('User [%s] is already in RiderGroup [%s]' % (validated_data['user'], validated_data['ridergroup']))

        membership = super(RiderGroupMembershipSerializer, self).create(validated_data)

        return membership

    class Meta:
        model = RiderGroupMembership
        fields = ('id', 'timestamp', 'ridergroup', 'user', 'url',)
        read_only_fields = ('timestamp',)


class RiderGroupInvitationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="user-detail", queryset=User.objects.all())
    ridergroup = serializers.HyperlinkedRelatedField(view_name="ridergroup-detail", queryset=RiderGroup.objects.all())
    accepted = serializers.BooleanField(required=False)

    def create(self, validated_data):
        if( RiderGroupInvitation.objects.filter(user=validated_data['user'], ridergroup=validated_data['ridergroup']).exists() ):
            raise ValidationError('User [%s] is already invited to RiderGroup [%s]' % (validated_data['user'], validated_data['ridergroup']))
        
        invitation = super(RiderGroupInvitationSerializer, self).create(validated_data)

        return invitation

    class Meta:
        model = RiderGroupInvitation
        fields = ('id', 'timestamp', 'ridergroup', 'accepted', 'user', 'url',)
        read_only_fields = ('timestamp',)

class RiderGroupRideMembershipSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)
    ridergroup = serializers.HyperlinkedRelatedField(view_name="ridergroup-detail", queryset=RiderGroup.objects.all())
    ride = serializers.HyperlinkedRelatedField(view_name="ride-detail", queryset=Ride.objects.all())

    def create(self, validated_data):
        if( RiderGroupRideMembership.objects.filter(ride=validated_data['ride'], ridergroup=validated_data['ridergroup']).exists() ):
            raise ValidationError('Ride [%s] is already in RiderGroup [%s]' % (validated_data['ride'], validated_data['ridergroup']))
        
        invitation = super(RiderGroupRideMembershipSerializer, self).create(validated_data)

        return invitation

    class Meta:
        model = RiderGroupRideMembership
        fields = ('id', 'timestamp', 'ridergroup', 'ride', 'creator', 'url',)
        read_only_fields = ('timestamp', 'creator')
