# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewMe', '0024_auto_20171112_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Randomizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tagger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
