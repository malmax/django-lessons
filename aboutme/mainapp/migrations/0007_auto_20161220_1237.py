# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20161220_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='address',
            field=models.CharField(default='+7(812)123-4567', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(default='+7(812)123-4567', max_length=20),
            preserve_default=False,
        ),
    ]
