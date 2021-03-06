# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='department',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='credit',
            name='job',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='info',
            name='budget',
            field=models.PositiveIntegerField(blank=True, help_text='Total budget in dollars', null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='original_title',
            field=models.CharField(blank=True, help_text='Title in original language', max_length=128),
        ),
        migrations.AlterField(
            model_name='info',
            name='revenue',
            field=models.PositiveIntegerField(blank=True, help_text='Total revenue in dollars', null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='revenue_ua',
            field=models.PositiveIntegerField(blank=True, help_text='Revenue in Ukraine', null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='tagline',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='info',
            name='vote_count',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='keywords',
            field=models.ManyToManyField(blank=True, to='common.KeyWord'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='production_companies',
            field=models.ManyToManyField(blank=True, to='common.ProductionCompany'),
        ),
    ]
