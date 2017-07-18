# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20170717_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(max_length=30)),
                ('discount_percent', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='basket',
            name='promo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Promo'),
        ),
    ]