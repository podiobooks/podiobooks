# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='awards',
            field=models.ManyToManyField(related_name='titles', to='core.Award', blank=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='payment_email_address',
            field=models.EmailField(help_text=b'Email address to send payments or tips for this title.', max_length=254, null=True, blank=True),
        ),
    ]
