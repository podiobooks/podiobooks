from django.db import models
from django.contrib.auth.models import User
import datetime
import pbsite


class UserProfile(models.Model):
	"""(UserProfile description)"""
	user = models.ForeignKey(User)
	status = models.IntegerField(default=1)
	email = models.EmailField()
	status = models.IntegerField(default=1)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "UserProfile"

class License(models.Model):
	"""(TitleLicense description)"""
	text = models.CharField(blank=False, max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	image_url = models.URLField(blank=False, verify_exists=True)
	code = models.TextField(blank=True)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.text

class Advisory(models.Model):
	"""(Advisory description)"""
	name = models.CharField(max_length=100)
	displaytext = models.CharField(max_length=255)
	hexcolor = models.CharField(max_length=6)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.name

class Series(models.Model):
	"""(Series description)"""
	name = models.CharField(blank=True, max_length=255)
	description = models.TextField()
	url = models.URLField(blank=True, verify_exists=True, null=True)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
		
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.name

class Award(models.Model):
	"""(Award description)"""
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

# replaced Author with Contributor 
class Contributor(models.Model):
	"""(Contributor description)"""
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	displayname = models.CharField(max_length=255)
	user = models.ForeignKey(User, null=True)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.displayname


class Title(models.Model):
	"""(Title description)"""
	
	name = models.CharField(max_length=255)
	series = models.ForeignKey(Series, null=True)
	description = models.TextField()
	slug = models.SlugField()
	cover = models.ImageField(upload_to=pbsite.settings.MEDIA_COVERS)
	status = models.IntegerField(default=1)
	license = models.ForeignKey(License, null=True)
	display_on_homepage = models.BooleanField(default = False)
	is_hosted_at_pb = models.BooleanField(default = True)
	advisory = models.ForeignKey(Advisory, null=True)
	is_adult = models.BooleanField(default=False)
	is_complete = models.BooleanField(default=False)
	avg_audio_quality = models.DecimalField(max_digits=5, decimal_places=3, default=0)
	avg_narration = models.DecimalField(max_digits=5, decimal_places=3, default=0)
	avg_writing = models.DecimalField(max_digits=5, decimal_places=3, default=0)
	avg_overall = models.DecimalField(max_digits=5, decimal_places=3, default=0)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	old_id = models.IntegerField(blank=True, null=True)
        contributors = models.ManyToManyField(Contributor, through='TitleContributors')
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.name

class ContributorType(models.Model):
        name=models.CharField(max_length=255)

class TitleContributors(models.Model):
        """(Contributor description)"""
        title = models.ForeignKey(Title)
        contributor = models.ForeignKey(Contributor)
        contributor_type = models.ForeignKey(ContributorType)
        

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

class Media(models.Model):
	"""(Media description)"""
	name = models.CharField(max_length=255)
	baseurl = models.CharField(max_length=255)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.name



class Promo(models.Model):
	"""(Promo description)"""
	title = models.ForeignKey(Title)
	display_text = models.CharField(max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	display_order = models.SmallIntegerField(blank=False, null=False, default=1)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return self.display_text
		
class Partner(models.Model):
	"""(Modelname description)"""
	name = models.CharField(blank=False, max_length=255)
	url = models.URLField(blank=False, verify_exists=True)
	logo = models.ImageField(upload_to="/dir/path")
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	old_id = models.IntegerField(blank=True, null=True)
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Modelname"

class TitleUrl(models.Model):
	"""(TitleUrls description)"""
	title = models.ForeignKey(Title)
	url = models.URLField(blank=False, verify_exists=True)
	linktext = models.CharField(blank=False, max_length=255)
	displayorder = models.SmallIntegerField(blank=False, null=False, default=1)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "TitleUrls"

class TitleAward(models.Model):
	"""(TitleAward description)"""
	title = models.ForeignKey(Title)
	award = models.ForeignKey(Award)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "TitleAward"

class TitleMedia(models.Model):
	"""(TitleMedia description)"""
	title = models.ForeignKey(Title)
	media = models.ForeignKey(Media)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "TitleMedia"

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

class Episode(models.Model):
	"""(Episode description)"""
	title = models.ForeignKey(Title)
	name = models.CharField(max_length=255)
	sequence = models.IntegerField(blank=False, null=False)
	description = models.TextField(blank=True)
	url = models.URLField(blank=False, verify_exists=True)
	filesize = models.IntegerField(default=0)
	status = models.SmallIntegerField(default=1)
	deleted = models.PositiveSmallIntegerField(default=0)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	old_id = models.IntegerField(blank=True, null=True)
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Episode"

		
class Category(models.Model):
	"""(Category description)"""
	name = models.CharField(max_length=255)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Category"
		
class TitleCategory(models.Model):
	"""(TitleCategory description)"""
	title = models.ForeignKey(Title)
	category = models.ForeignKey(Category)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "TitleCategory"


# Modified to handle alternate subscriptions
# relpace last_downloaded_episode with downloaded_episodes??
class Subscription(models.Model):
	"""(Subscription description)"""
#	title = models.ForeignKey(Title)
	user = models.ForeignKey(User)
	day_interval = models.SmallIntegerField(default=7)
	partner = models.ForeignKey(Partner)
	last_downloaded_episode = models.ForeignKey(Episode)
	last_downloaded_date = models.DateTimeField(blank=True, default=datetime.datetime.now())
	finished = models.PositiveSmallIntegerField(null=False, default=0)
	deleted = models.PositiveSmallIntegerField(null=False, default=0)
	date_created = models.DateTimeField(blank=False, default=datetime.datetime.now())
	date_updated = models.DateTimeField(blank=False, default=datetime.datetime.now())
	old_id = models.IntegerField(blank=True, null=True)
	
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Subscription"


class TitleSubscription(models.Model):
        subscription = models.ForeignKey(Subscription)
        title = models.ForeignKey(Title)

class SeriesSubscription(models.Model):
        subscription = models.ForeignKey(Subscription)
        series = models.ForeignKey(Series)

class ContributorSubscription(models.Model):
        subscription = models.ForeignKey(Subscription)
        contributor = models.ForeignKey(Contributor)
        contributor_types = models.ForeignKey(ContributorType)


# # TODO
# class Product(models.Model):
#         name = models.CharField(blank=False, max_length=255)
#         titles = models.ManyToManyField(Title,through='ProductTitles')
#         ## ??

# class ProductTitles(models.Model):
#         product = models.ForeignKey(Product)
#         title = models.ForeignKey(Title)
#         sequence =  models.IntegerField(blank=False, null=False)
        
