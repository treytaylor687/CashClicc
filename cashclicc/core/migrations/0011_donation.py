# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170910_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_donations', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
