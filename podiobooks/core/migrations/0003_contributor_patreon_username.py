# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150422_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='patreon_username',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
