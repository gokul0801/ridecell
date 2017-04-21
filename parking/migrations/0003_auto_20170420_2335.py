# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_spot_parkingstarttime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spot',
            old_name='parkingStarttime',
            new_name='parkingStartTime',
        ),
        migrations.AddField(
            model_name='spot',
            name='parkingAllocatedTime',
            field=models.FloatField(null=True),
        ),
    ]
