# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20161220_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='region',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
