# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-20 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20170719_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='promo',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]