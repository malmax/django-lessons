# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-28 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopbase', '0004_auto_20161228_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genrecategory',
            name='description',
            field=models.CharField(blank=True, max_length=100, verbose_name='Описание'),
        ),
    ]
