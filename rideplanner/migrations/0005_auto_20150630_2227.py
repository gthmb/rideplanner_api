# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rideplanner', '0004_auto_20150630_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riderlicensemembership',
            old_name='user',
            new_name='user_profile',
        ),
    ]
