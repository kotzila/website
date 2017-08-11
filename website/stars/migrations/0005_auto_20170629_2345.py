# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 23:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stars', '0004_auto_20170629_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='star',
            name='poster',
            field=models.ForeignKey(blank=True, help_text='main photo for this star', null=True, on_delete=django.db.models.deletion.CASCADE, to='images.Image'),
        ),
    ]
