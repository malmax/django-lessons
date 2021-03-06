# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_works_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='works',
            name='employerName',
        ),
        migrations.AddField(
            model_name='organization',
            name='region',
            field=models.CharField(default='Санкт-Петербург', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='works',
            name='endDate',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='title',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='works',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Должность'),
        ),
    ]
