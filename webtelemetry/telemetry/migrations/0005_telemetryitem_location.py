# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-07 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0004_auto_20161104_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='telemetryitem',
            name='location',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]