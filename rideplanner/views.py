from urlparse import urlparse

from django.contrib.auth.models import User
from django.db.models import Q

from rideplanner.models import (
    Ride, 
    UserProfile, 
    RideMembership,
    RideInvitation,
    RiderGroup,
    RiderGroupInvitation,
    RiderGroupMembership,
    RiderGroupRideMembership,
)

# from snippets.permissions import IsOwnerOrReadOnly
from rideplanner.serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    RideSerializer, 
    RideMembershipSerializer,
    RideInvitationSerializer,
    RiderGroupSerializer,
    RiderGroupInvitationSerializer,
    RiderGroupMembershipSerializer,
    RiderGroupRideMembershipSerializer,
)

from rest_framework import mixins, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.core.urlresolvers import resolve

from rest_framework.exceptions import ValidationError

from pprint import pprint

from rest_framework_extensions.mixins import NestedViewSetMixin

class UserViewSet( mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet( mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @list_route(methods=['get'])
    def me(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

class RideViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Ride.objects.all()
        else:
            return Ride.objects.filter(Q(creator = self.request.user.id)) # or is a participant

    @list_route(methods=['get'])
    def search(self, request):        
        rides = Ride.objects.filter(Q(creator = self.request.user.id) | Q(viewable_setting = 1)) # or is a participant
        serializer = RideSerializer(rides, many=True, context={'request': request})

        return Response(serializer.data)

class RideMembershipViewSet(viewsets.ModelViewSet):
    queryset = RideMembership.objects.all()
    serializer_class = RideMembershipSerializer

class RideInvitationViewSet(viewsets.ModelViewSet):
    queryset = RideInvitation.objects.all()
    serializer_class = RideInvitationSerializer

class RiderGroupViewSet(viewsets.ModelViewSet):
    queryset = RiderGroup.objects.all()
    serializer_class = RiderGroupSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return RiderGroup.objects.all()
        else:
            return RiderGroup.objects.filter(Q(creator = self.request.user.id)) # or is a member

    @list_route(methods=['get'])
    def search(self, request):        
        groups = RiderGroup.objects.filter(Q(creator = self.request.user.id) | Q(viewable_setting = 1)) # or is a member
        serializer = RiderGroupSerializer(rides, many=True, context={'request': request})

        return Response(serializer.data)

class RiderGroupInvitationViewSet(viewsets.ModelViewSet):
    queryset = RiderGroupInvitation.objects.all()
    serializer_class = RiderGroupInvitationSerializer

class RiderGroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = RiderGroupMembership.objects.all()
    serializer_class = RiderGroupMembershipSerializer

class RiderGroupRideMembershipViewSet(viewsets.ModelViewSet):
    queryset = RiderGroupRideMembership.objects.all()
    serializer_class = RiderGroupRideMembershipSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
