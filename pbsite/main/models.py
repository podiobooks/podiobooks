from django.db import models
from django.contrib.auth.models import User
import datetime
import pbsite

class Advisory(models.Model):
	"""(Advisory description)"""
	slug = models.SlugField()
	name = models.CharField(max_length=100)
	displaytext = models.CharField(max_length=255)
	hexcolor = models.CharField(max_length=6)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	# rather than storing a hex-color, would it make more sense to
	# add a css class 'Advisory_{slug}' for flexibility??

	class Admin:
		list_display = ('',)
		search_fields = ('',)
		
	class Meta:
		verbose_name_plural = "advisories"

	def __str__(self):
		return self.name

class Award(models.Model):
	"""(Award description)"""
	slug=models.SlugField()
	name = models.CharField(blank=True, max_length=255)
	url = models.URLField(blank=True, verify_exists=True, null=True)
	image = models.ImageField(upload_to=pbsite.settings.MEDIA_AWARDS)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.name

        @models.permalink
        def get_absolute_url(self):
                return ('award_detail', [self.slug])

class Category(models.Model):
	"""(Category description)"""
	name = models.CharField(max_length=255)
        slug = models.SlugField()
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)
		
	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name

        @models.permalink
        def get_absolute_url(self):
                return ('category_detail', [self.slug])

class Contributor(models.Model):
	"""(Contributor description)"""
	user = models.ForeignKey(User, null=True) #User is an OOTB Django Auth Model
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	displayname = models.CharField(max_length=255)
	slug=models.SlugField()
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	def __str__(self):
		return self.displayname

# ContributorSubscription is a little different in that you can
# declare multiple types, allowing you to say you want all items from
# contributor X where they are a contributor of type A, B, and C
class ContributorSubscription(models.Model):
	subscription = models.ForeignKey('Subscription')
	contributor = models.ForeignKey('Contributor')
	contributor_types = models.ManyToManyField('ContributorType')
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())

class ContributorType(models.Model):
	slug=models.SlugField()
	name=models.CharField(max_length=255)

        def __str__(self):
		return self.name

class Episode(models.Model):
	"""(Episode description)"""
	title = models.ForeignKey('Title')
	name = models.CharField(max_length=255)
	sequence = models.IntegerField(blank=False, null=False)
	description = models.TextField(blank=True)
	url = models.URLField(blank=False, verify_exists=True)
	filesize = models.IntegerField(default=0)
	status = models.SmallIntegerField(default=1)
	deleted = models.BooleanField(default=False)
	old_id = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Episode"

class License(models.Model):
	"""(TitleLicense description)"""
	slug=models.SlugField()
	text = models.CharField(blank=False, max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	image_url = models.URLField(blank=False, verify_exists=True)
	code = models.TextField(blank=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.text

class Media(models.Model):
	"""(Media description)"""
	title = models.ForeignKey('Title')
	name = models.CharField(max_length=255)
	baseurl = models.CharField(max_length=255)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	class Meta:
		verbose_name_plural = "media"

	def __str__(self):
		return self.name

class Partner(models.Model):
	"""(Modelname description)"""
	name = models.CharField(blank=False, max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	logo = models.ImageField(upload_to="/dir/path")
	deleted = models.BooleanField(default=False)
	old_id = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Modelname"

class Promo(models.Model):
	"""(Promo description)"""
	title = models.ForeignKey('Title')
	display_text = models.CharField(max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	display_order = models.SmallIntegerField(blank=False, null=False, default=1)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.display_text
		
class Series(models.Model):
	"""(Series description)"""
	slug = models.SlugField()
	name = models.CharField(blank=True, max_length=255)
	description = models.TextField()
	url = models.URLField(blank=True, verify_exists=True, null=True)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	class Admin:
		list_display = ('',)
		search_fields = ('',)
		
	class Meta:
		verbose_name_plural = "series"

	def __str__(self):
		return self.name

        @models.permalink
        def get_absolute_url(self):
                return ('series_detail', [self.slug])
	
# Modified to handle alternate subscriptions
# replace last_downloaded_episode with downloaded_episodes??
class Subscription(models.Model):
	"""A Subscription is when a user decides to add a particular title or series to their personal feed"""
	titles = models.ManyToManyField('Title')  # You can access the relationship from Title as title.subscription_set
	series = models.ManyToManyField('Series') # You can access the relationship from Series as series.subscription_set
	user = models.ForeignKey(User) #User is an OOTB Django Auth Model
	day_interval = models.SmallIntegerField(default=7)
	partner = models.ForeignKey('Partner')
	last_downloaded_episode = models.ForeignKey('Episode')
	last_downloaded_date = models.DateTimeField(blank=True, default=datetime.datetime.now())
	finished = models.PositiveSmallIntegerField(null=False, default=0)
	deleted = models.PositiveSmallIntegerField(null=False, default=0)
	old_id = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Subscription"

class Title(models.Model):
	"""Title is the central class, and represents the media item as a whole."""
	
	name = models.CharField(max_length=255)
	series = models.ForeignKey('Series', null=True, blank=True)
	description = models.TextField()
	slug = models.SlugField()
	cover = models.ImageField(upload_to=pbsite.settings.MEDIA_COVERS)
	status = models.IntegerField(default=1)
	license = models.ForeignKey('License', null=True, blank=True)
	display_on_homepage = models.BooleanField(default = False)
	is_hosted_at_pb = models.BooleanField(default = True)
	advisory = models.ForeignKey('Advisory', null=True, blank=True)
	is_adult = models.BooleanField(default=False)
	is_complete = models.BooleanField(default=False)
	avg_audio_quality = models.FloatField(default=0)
	avg_narration = models.FloatField(default=0)
	avg_writing = models.FloatField(default=0)
	avg_overall = models.FloatField(default=0)
	deleted = models.BooleanField(default=False)
	old_id = models.IntegerField(blank=True, null=True)
	contributors = models.ManyToManyField('Contributor', through='TitleContributors')
	categories = models.ManyToManyField('Category')
	awards = models.ManyToManyField('Award', blank=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.name

        @models.permalink
        def get_absolute_url(self):
                return ('title_detail', [self.slug])

class TitleContributors(models.Model):
	"""(Contributor description)"""
	title = models.ForeignKey('Title')
	contributor = models.ForeignKey('Contributor')
	contributor_type = models.ForeignKey('ContributorType')
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())

class TitleUrl(models.Model):
	"""(TitleUrls description)"""
	title = models.ManyToManyField('Title')
	url = models.URLField(blank=False, verify_exists=True)
	linktext = models.CharField(blank=False, max_length=255)
	displayorder = models.SmallIntegerField(blank=False, null=False, default=1)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "TitleUrls"

class UserProfile(models.Model):
	"""(UserProfile description)"""
	user = models.ForeignKey(User) #User is an OOTB Django Auth Model
	slug = models.SlugField()
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "UserProfile"

# class Author(models.Model):
# 	"""(Author description)"""
# 	firstname = models.CharField(max_length=255)
# 	lastname = models.CharField(max_length=255)
# 	displayname = models.CharField(max_length=255)
# 	user = models.ForeignKey(User, null=True)
# 	deleted = models.BooleanField(default=False)
# 	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
# 	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
# 	class Admin:
# 		list_display = ('',)
# 		search_fields = ('',)

# 	def __str__(self):
# 		return self.displayname

## class TitleAward(models.Model):
## 	"""(TitleAward description)"""
## 	title = models.ForeignKey(Title)
## 	award = models.ForeignKey(Award)
## 	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
## 	class Admin:
## 		list_display = ('',)
## 		search_fields = ('',)

## 	def __str__(self):
## 		return "TitleAward"

# class TitleMedia(models.Model):
#   """(TitleMedia description)"""
#   title = models.ForeignKey(Title)
#   media = models.ForeignKey(Media)
#   date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
## 	class Admin:
## 		list_display = ('',)
## 		search_fields = ('',)

## 	def __str__(self):
## 		return "TitleMedia"

# class TitleAuthor(models.Model):
# 	"""(TitleAuthor description)"""
# 	title = models.ForeignKey(Title)
# 	author = models.ForeignKey(Author)
# 	displayorder = models.IntegerField(blank=True, null=True)
# 	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
# 	class Admin:
# 		list_display = ('',)
# 		search_fields = ('',)

# 	def __str__(self):
# 		return "TitleAuthor"

# class TitleCategory(models.Model):
# 	"""(TitleCategory description)"""
# 	title = models.ForeignKey(Title)
# 	category = models.ForeignKey(Category)
# 	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
# 	class Admin:
# 		list_display = ('',)
# 		search_fields = ('',)

# 	def __str__(self):
# 		return "TitleCategory"

# # TODO
# class Product(models.Model):
#         name = models.CharField(blank=False, max_length=255)
#         titles = models.ManyToManyField(Title,through='ProductTitles')
#         ## ??

# class ProductTitles(models.Model):
#         product = models.ForeignKey(Product)
#         title = models.ForeignKey(Title)
#         sequence =  models.IntegerField(blank=False, null=False)
        

# set up emacs to be in line with ctmiller's editing style
# -*- mode: Python; indent-tabs-mode: 1; -*-
