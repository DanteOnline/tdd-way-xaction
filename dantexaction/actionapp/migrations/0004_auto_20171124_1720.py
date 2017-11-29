# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-24 14:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actionapp', '0003_action_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_actions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]