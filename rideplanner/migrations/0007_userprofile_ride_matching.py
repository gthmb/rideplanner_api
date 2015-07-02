# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rideplanner', '0006_auto_20150630_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ride_matching',
            field=models.BooleanField(default=False),
        ),
    ]
