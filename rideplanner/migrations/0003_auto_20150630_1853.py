# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rideplanner', '0002_ridercategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='category_cx',
            field=models.ForeignKey(related_name='rider_category_cx', default=1, to='rideplanner.RiderCategory'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category_mtb',
            field=models.ForeignKey(related_name='rider_category_mtb', default=1, to='rideplanner.RiderCategory'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category_road',
            field=models.ForeignKey(related_name='rider_category_road', default=1, to='rideplanner.RiderCategory'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category_track',
            field=models.ForeignKey(related_name='rider_category_track', default=1, to='rideplanner.RiderCategory'),
        ),
    ]
