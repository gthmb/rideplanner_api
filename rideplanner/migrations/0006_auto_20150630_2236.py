# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rideplanner', '0005_auto_20150630_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riderlicense',
            name='creator',
            field=models.ForeignKey(related_name='rider_license_creator', to='rideplanner.UserProfile'),
        ),
    ]
