# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 16:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ZSIV', '0025_auto_20160711_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summaries',
            old_name='IV',
            new_name='Inhaltsverzeichnis',
        ),
        migrations.RemoveField(
            model_name='summaries',
            name='Filename',
        ),
    ]