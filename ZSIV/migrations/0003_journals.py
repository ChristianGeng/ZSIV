# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZSIV', '0002_auto_20160701_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=400)),
            ],
        ),
    ]
