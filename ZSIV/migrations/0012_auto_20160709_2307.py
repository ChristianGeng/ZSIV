# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-09 21:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ZSIV', '0011_auto_20160704_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summaries',
            name='Created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 7, 9, 21, 7, 54, 512081, tzinfo=utc)),
        ),
    ]
