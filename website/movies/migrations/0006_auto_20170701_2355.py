# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20170701_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='vote_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
