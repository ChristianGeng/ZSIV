# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZSIV', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sykophanten',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Vorname', models.CharField(max_length=200)),
                ('Nachname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
