# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 21:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviewMe', '0012_feedback_raw_passivity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='raw_passivity',
        ),
    ]
