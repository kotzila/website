# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20170730_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='key',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='video',
            name='site',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='video',
            name='type',
            field=models.CharField(max_length=64),
        ),
    ]