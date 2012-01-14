"""Profile Module Models File"""

# pylint: disable=C0111,R0201,W0232

from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import datetime

class UserProfile(models.Model):
    """Information about the user which we need for preferences, social needs,
    etc."""
    user = models.ForeignKey(User, related_name='userprofile') #User is an OOTB Django Auth Model
    slug = models.SlugField()
    url = models.URLField(blank=True, verify_exists=True)
    twitter_username = models.CharField(max_length=50, blank=True)
    disqus_username = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, max_length=255, blank=True)
    short_profile = models.CharField(max_length=255)
    long_profile = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_updated = models.DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        verbose_name_plural = "User Profiles"
        
    def __unicode__(self):
        return "UserProfile for %s" % self.user.username

# This adds a property to the main User module enabling access to the profile as a property rather than a function
# This came from http://www.codekoala.com/blog/2009/quick-django-tip-user-profiles/    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
    
def create_userprofile_callback(sender, instance, **kwargs): # pylint: disable=W0613
    """Callback to automatically create a UserProfile whenever a user is created 
    - it's hooked in at the bottom of this file"""
    if kwargs.get('created'):
        UserProfile.objects.create(user=instance, slug=instance.username)

post_save.connect(create_userprofile_callback, sender=User, dispatch_uid="podiobooks.profile.UserProfile")
