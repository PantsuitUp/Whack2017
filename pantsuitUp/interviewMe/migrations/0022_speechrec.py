# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewMe', '0021_auto_20171111_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeechRec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output_text', models.CharField(default='', max_length=100000)),
            ],
        ),
    ]
