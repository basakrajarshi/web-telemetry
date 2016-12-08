# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clitelemetry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='args',
        ),
        migrations.RemoveField(
            model_name='event',
            name='path',
        ),
        migrations.AddField(
            model_name='event',
            name='audit_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='cmd',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateTimeField(),
        ),
    ]