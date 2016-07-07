# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_panorama_datetime_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='order',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='panorama',
            name='order',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]