# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160208_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rights_owner_email_address',
            field=models.EmailField(help_text=b'Email address of the Rights Owner.', max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='agreement_url',
            field=models.URLField(help_text=b'Full URL to Terms Agreement The Rights Owner Submitted', max_length=255, null=True, verbose_name=b'Agreement URL', blank=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='date_accepted',
            field=models.DateTimeField(null=True, verbose_name=b'Date Terms for this Title Accepted by Rights Owner', blank=True),
        ),
    ]
