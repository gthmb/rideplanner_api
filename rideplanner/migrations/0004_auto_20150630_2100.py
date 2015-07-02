# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rideplanner', '0003_auto_20150630_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiderLicense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=64)),
                ('creator', models.ForeignKey(related_name='rider_license_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RiderLicenseMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('license', models.ForeignKey(to='rideplanner.RiderLicense')),
                ('user', models.ForeignKey(to='rideplanner.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='RiderLicenseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='riderlicense',
            name='license_type',
            field=models.ForeignKey(to='rideplanner.RiderLicenseType'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='licenses',
            field=models.ManyToManyField(related_name='rider_license_membership', null=True, through='rideplanner.RiderLicenseMembership', to='rideplanner.RiderLicense', blank=True),
        ),
    ]
