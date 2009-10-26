from django.db import models
from django.contrib.auth.models import User
import datetime
import podiobooks

class Advisory(models.Model):
	"""Advisories are notifications about titles for the users. These could be
    viewed as not unlike movie ratings, but they are more descriptive. PB1
    has three, For Kids, Family Friendly, and Adult."""
	slug = models.SlugField()
	name = models.CharField(max_length=100)
	displaytext = models.CharField(max_length=255)
	hexcolor = models.CharField(max_length=6)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	# rather than storing a hex-color, would it make more sense to
	# add a css class 'Advisory_{slug}' for flexibility??
		
	class Meta:
		verbose_name_plural = "advisories"
		ordering = ['name']

	def __unicode__(self):
		return self.name

class Award(models.Model):
	"""Awards are just that: awards for a title, like winning a Parsec, etc."""
	slug = models.SlugField()
	name = models.CharField(blank=True, max_length=255)
	url = models.URLField(blank=True, verify_exists=True, null=True)
	image = models.ImageField(upload_to=podiobooks.settings.MEDIA_AWARDS)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('award_detail', [self.slug])

class Category(models.Model):
	"""Categories describe titles for easy of browsing and for recommendations."""
	slug = models.SlugField()
	name = models.CharField(max_length=255)
	# Note - titles are available as title_set.all()
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	class Meta:
		verbose_name_plural = "categories"
		ordering = ['name']

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('category_detail', [self.slug])

class Contributor(models.Model):
	"""A contributor is one who had done work on a title. For a book, it's an
    author or authors."""
	slug = models.SlugField()
	user = models.ForeignKey(User, null=True) #User is an OOTB Django Auth Model
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	displayname = models.CharField(max_length=255)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Meta:
		ordering = ['lastname', 'firstname']

	def __unicode__(self):
		return self.displayname
	
	@models.permalink
	def get_absolute_url(self):
		return ('contributor_detail', [self.slug])

class ContributorSubscription(models.Model):
	"""ContributorSubscription is a little different in that you can
	declare multiple types, allowing you to say you want all items from
	contributor X where they are a contributor of type A, B, and C"""
	subscription = models.ForeignKey('Subscription')
	contributor = models.ForeignKey('Contributor')
	contributor_types = models.ManyToManyField('ContributorType')
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())

class ContributorType(models.Model):
	"""Types of contributors: author, key grid, best boy, director, etc."""
	slug = models.SlugField()
	name = models.CharField(max_length=255)
	
	class Meta:
		verbose_name_plural = "Contributor Types"

	def __unicode__(self):
		return self.name

class Episode(models.Model):
	"""Titles are composed of Episodes. For a book, these are chapters or
    divisions of the book into smaller parts. For a comic book, it would be each
    issue of the comic."""
	title = models.ForeignKey('Title')
	name = models.CharField(max_length=255)
	sequence = models.IntegerField(blank=False, null=False)
	description = models.TextField(blank=True)
	url = models.URLField(blank=False, verify_exists=True)
	filesize = models.FloatField(default=0)
	status = models.SmallIntegerField(default=1)
	deleted = models.BooleanField(default=False)
	old_id = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return "Episode"
	
	@models.permalink
	def get_absolute_url(self):
		return ('episode_detail', [self.slug])

class License(models.Model):
	"""A collection of defined licenses for works. Creative Commons, All Rights
    Reserved, etc."""
	slug = models.SlugField()
	text = models.CharField(blank=False, max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	image_url = models.URLField(blank=False, verify_exists=True)
	code = models.TextField(blank=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Meta:
		ordering = ['slug']
	
	def __unicode__(self):
		return self.text

class Media(models.Model):
	"""Media are links to other forms of the title. In the case of books, these
    would be dead tree editions, epub, etc."""
	title = models.ForeignKey('Title')
	name = models.CharField(max_length=255)
	baseurl = models.CharField(max_length=255)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	class Meta:
		verbose_name_plural = "media"
		ordering = ['name']

	def __unicode__(self):
		return self.name

class Partner(models.Model):
	"""Partners are sites or organizations which contribute works to the system
    who wish to be recognized in some fashion (usually a graphic and link back
    to their site)."""
	name = models.CharField(blank=False, max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	logo = models.ImageField(upload_to="/dir/path")
	deleted = models.BooleanField(default=False)
	old_id = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return "Modelname"

class Promo(models.Model):
	"""Promotional materials for a title. Built to allow many types of
    material per a single title for folks what want to add some serious
    marketing mojo to their arsenal."""
	title = models.ForeignKey('Title')
	display_text = models.CharField(max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	display_order = models.SmallIntegerField(blank=False, null=False, default=1)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Meta:
		ordering = ['display_text']
	
	def __unicode__(self):
		return self.display_text

class Series(models.Model):
	"""Titles can belong to a series, wich allows for higher level grouping.
	Additionally, we might want to allow a setting to let users autosubscribe to
	the next book in a series automatically, or even just to subscribe to the
	series in one fell swoop."""
	slug = models.SlugField()
	name = models.CharField(max_length=255)
	description = models.TextField()
	url = models.URLField(blank=True, verify_exists=True, null=True)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	class Meta:
		verbose_name_plural = "series"
		ordering = ['name']

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('series_detail', [self.slug])

# Modified to handle alternate subscriptions
# replace last_downloaded_episode with downloaded_episodes??
class Subscription(models.Model):
	"""A Subscription is when a user decides to add a particular title or series
    to their personal feed. Subscriptions are released on a timed basis,
    allowing for dynamic construction and caching of customized feeds."""
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
	
	class Meta:
		ordering = ['user']
	
	def __unicode__(self):
		return "Subscription"

class Title(models.Model):
	"""Title is the central class, and represents the media item as a whole.i
    Example: A book. A season of a TV Series. A volume of a Comic Book. A set of
    college lectures."""

	name = models.CharField(max_length=255)
	series = models.ForeignKey('Series', null=True, blank=True)
	description = models.TextField()
	slug = models.SlugField()
	cover = models.ImageField(upload_to=podiobooks.settings.MEDIA_COVERS)
	status = models.IntegerField(default=1)
	license = models.ForeignKey('License', null=True, blank=True)
	display_on_homepage = models.BooleanField(default=False)
	is_hosted_at_pb = models.BooleanField(default=True)
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
	categories = models.ManyToManyField('Category', db_table="main_title_categories")
	awards = models.ManyToManyField('Award', blank=True)
	# Note: episodes are available as episode_set.all()
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	# Optionally configure Sphinx as search engine for titles
	if (podiobooks.settings.SEARCH_PROVIDER == 'SPHINX'):
		import djangosphinx.models
		search  = djangosphinx.models.SphinxSearch(index="pb2_titles")
	
	class Meta:
		ordering = ['name']
		
	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('title_detail', [self.slug])

class TitleContributors(models.Model):
	"""Join table to associate contributors to titles."""
	title = models.ForeignKey('Title')
	contributor = models.ForeignKey('Contributor')
	contributor_type = models.ForeignKey('ContributorType')
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Meta:
		verbose_name_plural = "Title Contributors"

class TitleUrl(models.Model):
	"""Allows us to have several links for a book, for display. For utility."""
	title = models.ManyToManyField('Title')
	url = models.URLField(blank=False, verify_exists=True)
	linktext = models.CharField(blank=False, max_length=255)
	displayorder = models.SmallIntegerField(blank=False, null=False, default=1)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	def __unicode__(self):
		return "TitleUrls"

class UserProfile(models.Model):
	"""Information about the user which we need for preferences, social needs,
    etc."""
	user = models.ForeignKey(User) #User is an OOTB Django Auth Model
	slug = models.SlugField()
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	def __unicode__(self):
		return "UserProfile"
# 
