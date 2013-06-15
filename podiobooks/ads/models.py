"""Podiobooks Main Models File"""

from __future__ import division
from django.db import models
from podiobooks.core.models import Episode, Title

# pylint: disable=C0111,R0201,W0232


class AdSchedule(models.Model):
    """Ad Schedules Control What Ads Get Inserted Where For A Title."""
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)

    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Ad Schedules"

    def __unicode__(self):
        return self.name


class AdSchedulePosition(models.Model):
    """Many-To-Many Intersection Entity Between An Ad Episode and An Ad Schedule."""
    ad_schedule = models.ForeignKey('AdSchedule', related_name='ad_schedule_positions')
    episode = models.ForeignKey(Episode, related_name='ad_schedule_episodes')
    sequence = models.IntegerField()

    class Meta:
        verbose_name_plural = "Ad Schedule Positions"

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ad_schedule__name']

    def __unicode__(self):
        return self.ad_schedule__name


class AdScheduleTitle(models.Model):
    """Ad Schedules Many To Many With Titles."""
    ad_schedule = models.ForeignKey('AdSchedule', related_name='titles')
    title = models.ForeignKey(Title, related_name='ad_schedules')

    # Note - titles are available as titles.all()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ad Schedule Titles"

    def __unicode__(self):
        return self.name