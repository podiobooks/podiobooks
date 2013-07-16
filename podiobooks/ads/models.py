"""Podiobooks Main Models File"""

from __future__ import division
from django.db import models
from podiobooks.core.models import Episode, Title
import datetime
from django.utils import timezone

# pylint: disable=C0111,R0201,W0232


class AdSchedule(models.Model):
    """Ad Schedules Control What Ads Get Inserted Where For A Title."""
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)

    deleted = models.BooleanField(default=False)
    date_start = models.DateTimeField(help_text="Date/Time Ad Schedule Should Begin To Appear In Feeds.")
    date_end = models.DateTimeField(help_text="Date/Time Ad Schedule Should Expire (Use Year 01-JAN-2100 For No Expire).")
    priority = models.IntegerField(default=10, help_text="Higher Numbers Will Insert Earlier If Conflict.")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    titles = models.ManyToManyField(Title, null=True, blank=True, related_name='ad_schedules')

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


### UTILITY FUNCTIONS
def get_active_ad_schedules_for_title(title):
    """Return a list of active ad schedules for a title"""

    ad_schedule_list = title.ad_schedules.filter(date_start__lte=datetime.datetime.now(timezone.utc),
                                                 date_end__gte=datetime.datetime.now(timezone.utc))

    return ad_schedule_list


def get_ep_list_with_ads_for_title(title):
    """Return a list of episodes with ad inserts for a title"""

    episode_list = list(title.episodes.all())
    ad_schedule_positions = AdSchedulePosition.objects.filter(ad_schedule__in=get_active_ad_schedules_for_title(title))
    for position in ad_schedule_positions:
        episode_list.insert(position.sequence - 1, position.episode)  # sequence - 1 since .insert inserts after

    return episode_list