# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-30 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='tmdb_id',
        ),
        migrations.AddField(
            model_name='country',
            name='iso_3166_1',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_en',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]