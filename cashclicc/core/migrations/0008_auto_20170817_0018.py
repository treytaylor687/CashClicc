# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 00:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170811_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_top_user',
            field=models.CharField(default='PLAY NOW!', max_length=50),
        ),
    ]
