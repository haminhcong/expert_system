# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 20:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert_system', '0006_rule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rulemodel',
            name='left',
        ),
    ]
