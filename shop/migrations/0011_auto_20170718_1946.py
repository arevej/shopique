# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20170718_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_ammount',
            field=models.FloatField(),
        ),
    ]
