# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20170127_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='lists.List'),
        ),
    ]
