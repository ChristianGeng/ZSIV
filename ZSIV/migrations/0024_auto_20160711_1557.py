# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 13:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ZSIV', '0023_summaries_iv'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summaries',
            old_name='CreationDate',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='summaries',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 7, 11, 13, 57, 48, 188382, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
