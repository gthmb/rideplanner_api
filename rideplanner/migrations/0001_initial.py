# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Ride',
                'verbose_name_plural': 'Rides',
            },
        ),
        migrations.CreateModel(
            name='RideInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('accepted', models.BooleanField(default=False)),
                ('ride', models.ForeignKey(to='rideplanner.Ride')),
            ],
            options={
                'verbose_name': 'RideInvitation',
                'verbose_name_plural': 'RideInvitations',
            },
        ),
        migrations.CreateModel(
            name='RideMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('ride', models.ForeignKey(to='rideplanner.Ride')),
            ],
            options={
                'verbose_name': 'RideMembership',
                'verbose_name_plural': 'RideMemberships',
            },
        ),
        migrations.CreateModel(
            name='RidePace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('value', models.IntegerField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='RideRepeatType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='RiderGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'RiderGroup',
                'verbose_name_plural': 'RiderGroups',
            },
        ),
        migrations.CreateModel(
            name='RiderGroupInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('accepted', models.BooleanField(default=False)),
                ('ridergroup', models.ForeignKey(to='rideplanner.RiderGroup')),
            ],
            options={
                'verbose_name': 'RiderGroupInvitation',
                'verbose_name_plural': 'RiderGroupInvitations',
            },
        ),
        migrations.CreateModel(
            name='RiderGroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('ridergroup', models.ForeignKey(to='rideplanner.RiderGroup')),
            ],
            options={
                'verbose_name': 'RiderGroupMembership',
                'verbose_name_plural': 'RiderGroupMemberships',
            },
        ),
        migrations.CreateModel(
            name='RiderGroupRideMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'RiderGroupRide',
                'verbose_name_plural': 'RiderGroupRides',
            },
        ),
        migrations.CreateModel(
            name='RideRouteType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='RideStateType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserGender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='UserPrivacySetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('age', models.IntegerField(max_length=2, null=True, blank=True)),
                ('gender', models.ForeignKey(blank=True, to='rideplanner.UserGender', null=True)),
                ('privacy_setting', models.ForeignKey(related_name='user_privacy_setting', default=1, to='rideplanner.UserPrivacySetting')),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.AddField(
            model_name='ridergroupridemembership',
            name='creator',
            field=models.ForeignKey(related_name='ridergroupmembership_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ridergroupridemembership',
            name='ride',
            field=models.ForeignKey(to='rideplanner.Ride'),
        ),
        migrations.AddField(
            model_name='ridergroupridemembership',
            name='ridergroup',
            field=models.ForeignKey(to='rideplanner.RiderGroup'),
        ),
        migrations.AddField(
            model_name='ridergroupmembership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ridergroupinvitation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ridergroup',
            name='creator',
            field=models.ForeignKey(related_name='ridergroup_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ridergroup',
            name='editable_setting',
            field=models.ForeignKey(related_name='ridergroup_editable_setting', default=1, to='rideplanner.AccessSetting'),
        ),
        migrations.AddField(
            model_name='ridergroup',
            name='invitees',
            field=models.ManyToManyField(related_name='ridergroup_invitees', null=True, through='rideplanner.RiderGroupInvitation', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='ridergroup',
            name='participants',
            field=models.ManyToManyField(related_name='ridergroup_participants', null=True, through='rideplanner.RiderGroupMembership', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='ridergroup',
            name='rides',
            field=models.ManyToManyField(related_name='rides', null=True, through='rideplanner.RiderGroupRideMembership', to='rideplanner.Ride', blank=True),
        ),
        migrations.AddField(
            model_name='ridergroup',
            name='viewable_setting',
            field=models.ForeignKey(related_name='ridergroup_viewable_setting', default=1, to='rideplanner.AccessSetting'),
        ),
        migrations.AddField(
            model_name='ridemembership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rideinvitation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ride',
            name='creator',
            field=models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ride',
            name='editable_setting',
            field=models.ForeignKey(related_name='ride_editable_setting', default=1, to='rideplanner.AccessSetting'),
        ),
        migrations.AddField(
            model_name='ride',
            name='invitees',
            field=models.ManyToManyField(related_name='ride_invitees', null=True, through='rideplanner.RideInvitation', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='pace',
            field=models.ForeignKey(related_name='ride_pace', default=1, to='rideplanner.RidePace'),
        ),
        migrations.AddField(
            model_name='ride',
            name='participants',
            field=models.ManyToManyField(related_name='ride_participants', null=True, through='rideplanner.RideMembership', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='repeat',
            field=models.ForeignKey(related_name='ride_repeat', default=1, to='rideplanner.RideRepeatType'),
        ),
        migrations.AddField(
            model_name='ride',
            name='ridergroups',
            field=models.ManyToManyField(related_name='rider_groups', null=True, through='rideplanner.RiderGroupRideMembership', to='rideplanner.RiderGroup', blank=True),
        ),
        migrations.AddField(
            model_name='ride',
            name='route_type',
            field=models.ForeignKey(related_name='ride_route', default=1, to='rideplanner.RideRouteType'),
        ),
        migrations.AddField(
            model_name='ride',
            name='state',
            field=models.ForeignKey(related_name='ride_state', default=1, to='rideplanner.RideStateType'),
        ),
        migrations.AddField(
            model_name='ride',
            name='viewable_setting',
            field=models.ForeignKey(related_name='ride_viewable_setting', default=1, to='rideplanner.AccessSetting'),
        ),
    ]
