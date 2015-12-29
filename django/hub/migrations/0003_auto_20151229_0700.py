# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0002_remove_project_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='branch',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='query',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
