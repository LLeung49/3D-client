# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_task_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='submit_time',
            field=models.CharField(default='2016-Oct-07 11:10:09', max_length=50),
        ),
    ]
