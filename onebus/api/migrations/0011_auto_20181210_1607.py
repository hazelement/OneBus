# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-12-10 23:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20181210_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stoptime',
            name='stop_id',
        ),
        migrations.RemoveField(
            model_name='stoptime',
            name='trip_id',
        ),
        migrations.AddField(
            model_name='stoptime',
            name='stop',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.Stop'),
        ),
        migrations.AddField(
            model_name='stoptime',
            name='trip',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.Trip'),
        ),
        migrations.AlterUniqueTogether(
            name='stoptime',
            unique_together=set([('trip', 'stop', 'stop_sequence')]),
        ),
    ]