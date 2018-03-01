# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-14 09:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fOn', '0004_auto_20170613_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unlike',
            name='unliked_post',
        ),
        migrations.AddField(
            model_name='unlike',
            name='unliked_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fOn.Post'),
        ),
    ]
