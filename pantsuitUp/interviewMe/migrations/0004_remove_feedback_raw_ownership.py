# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 21:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviewMe', '0003_auto_20171111_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='raw_ownership',
        ),
    ]