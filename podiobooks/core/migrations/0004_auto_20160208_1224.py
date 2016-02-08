# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_contributor_patreon_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='agreement_url',
            field=models.URLField(help_text=b'Full URL to Agreement The Rights Holder Submitted', max_length=255, null=True, verbose_name=b'Agreement URL', blank=True),
        ),
        migrations.AddField(
            model_name='title',
            name='rights_owner',
            field=models.CharField(help_text=b'Name of the Person or Entity that Owns the Rights to this Audiobook', max_length=255, null=True, verbose_name=b'Rights Owner', blank=True),
        ),
    ]
