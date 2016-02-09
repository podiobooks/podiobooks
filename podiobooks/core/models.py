"""Podiobooks Main Models File"""

from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from noodles.models import DefinedWidthsAssetsFromImagesMixin

# pylint: disable=C0111,R0201,W0232,W1001


class Award(models.Model):
    """Awards are just that: awards for a title, like winning a Parsec, etc."""
    slug = models.SlugField()
    name = models.CharField(blank=True, max_length=255)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='images/awards', max_length=255)
    # Note - titles are available as titles.all()
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'award_detail', [self.slug]


class Category(models.Model):
    """Categories describe titles for easy of browsing and for recommendations."""
    slug = models.SlugField(max_length=50)
    name = models.CharField(max_length=50)
    # Note - titles are available as title_set.all()
    # Note - for SQL purposes, titles are 'title'
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name_plural = "categories"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'category_detail', [self.slug]


class Contributor(models.Model):
    """A contributor is one who had done work on a title. For a book, it's an
    author or authors."""
    slug = models.SlugField(max_length=1000, db_index=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='contributor_info')  # User is an OOTB Django Auth Model
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=1024, blank=True)
    community_handle = models.CharField(max_length=255, blank=True)
    patreon_username = models.CharField(max_length=255, blank=True)
    scribl_username = models.CharField(max_length=255, blank=True)
    deleted = models.BooleanField(default=False)
    # Note: Titles are available a title_set.all()
    # Note: TitleContributor Objects (intermediate table) are available as titlecontributors.all()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['last_name', 'first_name']

    def __unicode__(self):
        return self.display_name

    @models.permalink
    def get_absolute_url(self):
        return 'contributor_detail', [self.slug]


class ContributorType(models.Model):
    """Types of contributors: author, narrator, key grip, best boy, director, etc."""
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    byline_text = models.CharField(max_length=255)
    # Note: TitleContributor Objects (intermediate table) are available as titlecontributors.all()

    class Meta(object):
        verbose_name_plural = "Contributor Types"

    def __unicode__(self):
        return self.name


class Episode(models.Model):
    """
    Titles are composed of Episodes. For a book, these are chapters or
    divisions of the book into smaller parts. For a comic book, it would be each
    issue of the comic.
    """
    title = models.ForeignKey('Title', related_name='episodes')
    name = models.CharField(max_length=255)
    sequence = models.IntegerField()  # Order in the Story
    description = models.TextField(blank=True)
    url = models.URLField()
    filesize = models.IntegerField(default=0,
                                   help_text="In bytes, corresponds to 'length' in RSS feed")  # Size of the media file
    duration = models.CharField(max_length=20, default='45:00',
                                help_text='Duration of the media file in minutes:seconds')  # Length of the media file (in minutes)
    contributors = models.ManyToManyField('Contributor', through='EpisodeContributor')
    deleted = models.BooleanField(default=False, db_index=True)
    media_date_created = models.DateTimeField(blank=True, null=True,
                                              help_text='Date the media file was added (e.g. to Libsyn)')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['title__name', 'sequence']

    def __unicode__(self):
        return u'Episode #{0}: {1}'.format(self.sequence, self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'episode_detail', [self.id]  # pylint: disable=E1101

    def _get_filesize_mb(self):
        return round(self.filesize / 1024.0 / 1024.0, 2)

    filesize_mb = property(_get_filesize_mb)


class EpisodeContributor(models.Model):
    """Join table to associate contributors to titles."""
    episode = models.ForeignKey('Episode', related_name='episodecontributors')
    contributor = models.ForeignKey('Contributor', related_name='episodecontributors')
    contributor_type = models.ForeignKey('ContributorType', related_name='episodecontributors')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name_plural = "Episode Contributors"


class License(models.Model):
    """A collection of defined licenses for works. Creative Commons, All Rights
    Reserved, etc."""
    slug = models.SlugField()
    text = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    code = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['slug']

    def __unicode__(self):
        return self.slug


MEDIA_NAME_CHOICES = (
    ('Print Version', 'Print Version'),
    ('Kindle Version', 'Kindle Version'),
    ('Smashwords Version', 'Smashwords Version'),
)


class Media(models.Model):
    """Media are links to other forms of the title. In the case of books, these
    would be dead tree editions, epub, etc."""
    title = models.ForeignKey('Title', related_name='media')
    name = models.CharField(max_length=255, default='Print Version', choices=MEDIA_NAME_CHOICES)
    identifier = models.CharField(max_length=255, blank=True, help_text="ISBN or Product ID")
    url = models.CharField(max_length=255, blank=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name_plural = "media"
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    """The last rating that was loaded from the pb1 site"""
    last_rating_id = models.IntegerField(default=0, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        get_latest_by = 'date_created'

    def __unicode__(self):
        return str(self.last_rating_id)


class Series(models.Model):
    """Titles can belong to a series, which allows for higher level grouping."""
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name_plural = "series"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'series_detail', [self.slug]


class Title(DefinedWidthsAssetsFromImagesMixin, models.Model):
    """Title is the central class, and represents the media item as a whole.
    Example: A book. A season of a TV Series. A volume of a Comic Book. A set of
    college lectures."""

    name = models.CharField(max_length=255)
    series = models.ForeignKey('Series', null=True, blank=True, related_name='titles')
    series_sequence = models.IntegerField(default=1, verbose_name='Series Sequence')
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    old_slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    cover = models.ImageField(max_length=500, upload_to='images/covers', blank=True, null=True)
    license = models.ForeignKey('License', null=True, related_name='titles')
    display_on_homepage = models.BooleanField(default=False, db_index=True, verbose_name='Disp. On Homepage')
    is_adult = models.BooleanField(default=False, db_index=True, verbose_name='Is Adult')
    is_explicit = models.BooleanField(default=False, db_index=True, verbose_name='Is Explicit')
    is_family_friendly = models.BooleanField(default=False, db_index=True, verbose_name='Is Family Friendly')
    is_for_kids = models.BooleanField(default=False, db_index=True, verbose_name='Is For Kids')
    language = models.CharField(max_length=10, default='en-us', db_index=True, help_text='Language Code for Title')
    promoter_count = models.IntegerField(default=0, db_index=True)
    detractor_count = models.IntegerField(default=0, db_index=True)
    deleted = models.BooleanField(default=False, verbose_name='Deleted?', db_index=True)
    contributors = models.ManyToManyField('Contributor',
                                          through='TitleContributor')  # related_name doesn't work with manual through
    # Note: TitleContributor Objects (intermediate table) are available as titlecontributors.all()
    byline = models.CharField(max_length=1024, blank=True)  # This is a formatted cache of the title contributors
    categories = models.ManyToManyField('Category',
                                        through='TitleCategory')  # related_name doesn't work with manual through tables
    # Note: TitleCategory Objects (intermediate table) are available as titlecategories.all()
    category_list = models.CharField(max_length=1024, blank=True)  # This is a formatted cache of the categories
    awards = models.ManyToManyField('Award', blank=True, related_name='titles')
    libsyn_show_id = models.CharField(max_length=50, db_index=True, blank=True, verbose_name='LibSyn Show ID',
                                      help_text='Starts with k-')
    libsyn_slug = models.SlugField(max_length=50, db_index=True, blank=True, verbose_name='LibSyn Slug',
                                   help_text='Show Slug from Libsyn')
    libsyn_cover_image_url = models.URLField(max_length=500, null=True, blank=True,
                                             verbose_name='Libsyn Cover Image URL',
                                             help_text='Full URL to Libsyn-hosted cover image.')
    itunes_adam_id = models.IntegerField(null=True, blank=True, verbose_name='iTunes ADAM Id',
                                         help_text='From iTunes Page URL for Podcast')
    itunes_new_feed_url = models.BooleanField(default=False, verbose_name='iTunes New Feed Url Tag',
                                              help_text='Include <itunes:new_feed_url> tag in feed (Required if you are changing the slug)')
    podiobooker_blog_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='Blog URL',
                                           help_text='Full URL to Blog Post Announcing Book - Used to Pull Comments')
    rights_owner = models.CharField(max_length=255, null=True, blank=True, verbose_name='Rights Owner',
                                           help_text='Name of the Person or Entity that Owns the Rights to this Audiobook')
    rights_owner_email_address = models.EmailField(null=True, blank=True,
                                              help_text='Email address of the Rights Owner.')
    agreement_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='Agreement URL',
                                           help_text='Full URL to Terms Agreement The Rights Owner Submitted')
    date_accepted = models.DateTimeField(null=True, blank=True,
                                         verbose_name='Date Terms for this Title Accepted by Rights Owner')
    tips_allowed = models.BooleanField(default=True, verbose_name='Collect Tips for this Title')
    payment_email_address = models.EmailField(null=True, blank=True,
                                              help_text='Email address to send payments or tips for this title.')
    scribl_book_id = models.CharField(null=True, blank=True, max_length=20, verbose_name='Scribl Book Id')
    scribl_allowed = models.BooleanField(default=True, verbose_name='Show this Title on Scribl')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date Created')
    date_updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date Updated')

    # Note: episodes are available as episodes.all()
    # Note: media are available as media.all()
    # Note: promos are available as promos.all()

    class Meta(object):
        ordering = ['name']

    def __unicode__(self):
        return self.slug

    def get_dimensions(self):
        return [100, 300, 900, 1400]
        
    def get_quality(self):
        return 85

    @models.permalink
    def get_absolute_url(self):
        return ('title_detail', [self.slug])

    @models.permalink
    def get_rss_feed_url(self):
        return ('title_episodes_feed', [self.slug])

    def net_promoter_score(self):
        total_count = self.promoter_count + self.detractor_count
        if total_count:
            return int((self.promoter_count / total_count) * 100)
        else:
            return 0

    def description_br(self):
        return self.description.replace('\n', '\n<br/>')  # pylint: disable=E1101

    def computed_rating(self):
        nps = self.net_promoter_score() / 100
        return nps * 5

    def get_byline(self):
        """ return a text-only byline (i.e. no HTML) """
        ret = ""
        for (i, title_contributor) in enumerate(self.titlecontributors.all()):
            if title_contributor.contributor_type.slug == "author":
                if i == 0:
                    ret += "by "
                elif i != len(self.titlecontributors.all()):
                    ret += ", "
                else:
                    ret = ""
            else:
                ret += title_contributor.contributor_type.byline_text + " "

            ret += title_contributor.contributor.__unicode__()
            ret += " "
        ret = ret.replace("  ", " ")
        return ret


class TitleCategory(models.Model):
    """
        Join table to associate categories to titles.
        This is built as a non-automatic model in order to get the signal hooks to work
    """
    title = models.ForeignKey('Title', related_name='titlecategories')
    category = models.ForeignKey('Category', related_name='titlecategories')

    class Meta(object):
        verbose_name_plural = "Title Categories"


# pylint: disable=W0613
def update_category_list(sender, instance, **kwargs):
    """ Update category list cache on titles when a new title category is added.
        Hooked to pre_save trigger for titlecategory below """
    categories = instance.title.categories.all()
    category_list = render_to_string('core/title/title_category_list.html', {'categories': categories, })

    instance.title.category_list = category_list
    instance.title.save()


post_save.connect(update_category_list, sender=TitleCategory)


class TitleContributor(models.Model):
    """Join table to associate contributors to titles."""
    title = models.ForeignKey('Title', related_name='titlecontributors')
    contributor = models.ForeignKey('Contributor', related_name='titlecontributors')
    contributor_type = models.ForeignKey('ContributorType', related_name='titlecontributors')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name_plural = "Title Contributors"
        ordering = ['contributor_type__slug', 'date_created']

    def __unicode__(self):
        return str(self.pk)


class TitleUrl(models.Model):
    """Allows us to have several links for a book, for display. For utility."""
    title = models.ForeignKey('Title', related_name='urls')
    url = models.URLField()
    linktext = models.CharField(max_length=255)
    displayorder = models.IntegerField(null=False, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url
