# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-23 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20170720_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='buyer_email',
            field=models.EmailField(default='', max_length=30),
            preserve_default=False,
        ),
    ]