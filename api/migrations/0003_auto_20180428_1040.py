# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180428_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calender',
            name='start_date',
            field=models.DateField(),
        ),
    ]
