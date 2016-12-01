# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-03 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0002_telemetryitem_element'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telemetryitem',
            name='event_type',
            field=models.CharField(choices=[('click', 'click'), ('keypress', 'keypress')], max_length=10),
        ),
    ]
