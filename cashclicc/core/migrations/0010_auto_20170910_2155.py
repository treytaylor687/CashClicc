# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20170821_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tokens',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
