# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewMe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='raw_ownership',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AddField(
            model_name='feedback',
            name='raw_passivity',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AddField(
            model_name='feedback',
            name='raw_personality',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AddField(
            model_name='feedback',
            name='raw_sentiment',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=3),
        ),
    ]
