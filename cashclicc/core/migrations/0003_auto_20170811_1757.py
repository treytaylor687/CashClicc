# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default=1111111111, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='validation_token',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='current_top_user',
            field=models.CharField(default='Clicc to Play!', max_length=50),
        ),
    ]
