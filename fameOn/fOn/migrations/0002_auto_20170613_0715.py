# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-13 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fOn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='liked_post',
        ),
        migrations.AddField(
            model_name='like',
            name='liked_post',
            field=models.ManyToManyField(to='fOn.Post'),
        ),
        migrations.AlterField(
            model_name='unlike',
            name='unliked_post',
            field=models.ManyToManyField(to='fOn.Post'),
        ),
    ]
