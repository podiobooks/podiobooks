# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150422_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('date_start', models.DateTimeField(help_text=b'Date/Time Ad Schedule Should Begin To Appear In Feeds.')),
                ('date_end', models.DateTimeField(help_text=b'Date/Time Ad Schedule Should Expire (Use Year 01-JAN-2100 For No Expire).')),
                ('priority', models.IntegerField(default=10, help_text=b'Higher Numbers Will Insert Earlier If Conflict.')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('titles', models.ManyToManyField(related_name='ad_schedules', to='core.Title', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Ad Schedules',
            },
        ),
        migrations.CreateModel(
            name='AdSchedulePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('ad_schedule', models.ForeignKey(related_name='ad_schedule_positions', to='ads.AdSchedule')),
                ('episode', models.ForeignKey(related_name='ad_schedule_episodes', to='core.Episode')),
            ],
            options={
                'ordering': ['ad_schedule__name'],
                'verbose_name_plural': 'Ad Schedule Positions',
            },
        ),
    ]
