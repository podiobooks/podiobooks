"""Profile Module Models File"""

from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime


class UserProfile(models.Model):
    """Information about the user which we need for preferences, social needs,
    etc."""
    user = models.ForeignKey(User, related_name='userprofile') #User is an OOTB Django Auth Model
    slug = models.SlugField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_updated = models.DateTimeField(default=datetime.datetime.now())
        
    def __unicode__(self):
        return "UserProfile for %s" % self.user.username
    
def create_userprofile_callback(sender, instance, **kwargs):
    """Callback to automatically create a UserProfile whenever a user is created 
    - it's hooked in at the bottom of this file"""
    if kwargs.get('created'):
        UserProfile.objects.create(user=instance, slug=instance.username)

post_save.connect(create_userprofile_callback, sender=User, dispatch_uid="podiobooks.profile.UserProfile")