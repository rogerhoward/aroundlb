# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20160402_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panorama',
            name='latitude',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='panorama',
            name='longitude',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
    ]
