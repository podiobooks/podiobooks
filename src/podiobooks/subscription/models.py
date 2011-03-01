"""Podiobooks Subscription Models File"""

from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from podiobooks.main.models import Episode, Title
import datetime

# pylint: disable=C0111,R0201,W0232

class TitleSubscription(models.Model):
    """
    A TitleSubscription is when a user decides to add a particular title
    to their personal feed. TitleSubscriptions are released on a timed basis,
    allowing for dynamic construction and caching of customized feeds.
    """
    title = models.ForeignKey(Title, related_name='subscriptions')  # You can access the relationship from Title as title.subscriptions
    user = models.ForeignKey(User, related_name='title_subscriptions') #User is an OOTB Django Auth Model
    day_interval = models.IntegerField(default=7)
    last_downloaded_episode = models.ForeignKey(Episode, related_name='title_subscriptions')
    last_downloaded_date = models.DateTimeField(null=True)
    finished = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_updated = models.DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        ordering = ['-date_created']
        unique_together = ('title', 'user')
    
    def __unicode__(self):
        return "%s is subscribed to %s every %d days" % (self.user.username, self.title.name, self.day_interval)
