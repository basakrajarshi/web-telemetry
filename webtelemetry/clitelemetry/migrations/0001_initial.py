# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cwd', models.CharField(max_length=1024)),
                ('time', models.DateTimeField()),
                ('cmd', models.CharField(max_length=32)),
                ('args', models.TextField(blank=True, null=True)),
                ('exit', models.CharField(max_length=48)),
                ('success', models.BooleanField()),
                ('path', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('user', models.CharField(max_length=24)),
                ('terminal', models.CharField(max_length=24)),
                ('host', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clitelemetry.Session'),
        ),
    ]
