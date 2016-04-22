"""Automated unit tests for the Podiobooks model classes"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase
from podiobooks.core.models import *  # @UnusedWildImport
from django.template.defaultfilters import slugify
from django.db.models import Count


class TitleTestCase(TestCase):
    """Test the Podiobooks Models from a Title-Centric POV"""

    def setUp(self):
        # This method sets up a whole series of model objects, and then tries to connect them together.

        # Create Some Test Users
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
        self.user3 = User.objects.create_user('testuser3', 'testuser3@test.com', 'testuser3password')

        # Create Some Series
        self.series1 = Series.objects.create(
            name="Podiobooks Series #1",
            description="A wonderful sample series that contains many fine books",
        )
        self.series1.slug = slugify(self.series1.name)
        self.series1.save()

        self.series2 = Series.objects.create(
            name="Podiobooks Series #2",
            description="Another wonderful sample series that contains many fine books",
        )
        self.series2.slug = slugify(self.series2.name)
        self.series2.save()

        # Create Some Titles
        self.title1 = Title.objects.create(
            name="Podiobooks Title #1",
            slug=slugify("Podiobooks Title #1"),
            series=self.series1,
            description="A fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
            cover="PodioBook Cover",
            display_on_homepage=True,
            is_adult=False,
            is_explicit=True,
            promoter_count=211,
            detractor_count=100,
        )

        self.title2 = Title.objects.create(
            name="Podiobooks Title #2",
            slug=slugify("Podiobooks Title #2"),
            series=self.series1,
            description="A second fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
            cover="PodioBook Cover 2",
            display_on_homepage=True,
            is_adult=False,
            is_explicit=False,
            promoter_count=123,
            detractor_count=4,
        )

        self.title3 = Title.objects.create(
            name="Podiobooks Title #3",
            slug=slugify("Podiobooks Title #3"),
            series=self.series2,
            description="A third fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
            cover="PodioBook Cover 3",
            display_on_homepage=True,
            is_adult=False,
            is_explicit=False,
            promoter_count=4,
            detractor_count=0,
        )

        # Create some Episodes
        self.episode1 = Episode.objects.create(
            title=self.title1,
            name="Podiobooks Title #1 Episode #1",
            sequence=1,
            description="This is the first wonderful episode of the test title1!",
            url="http://www.Podiobooks.com",
            filesize=328886,
        )

        self.episode2 = Episode.objects.create(
            title=self.title2,
            name="Podiobooks Title #2 Episode #1",
            sequence=1,
            description="This is the first wonderful episode of the test title2!",
            url="http://www.Podiobooks.com",
            filesize=32886,
        )

        self.episode3 = Episode.objects.create(
            title=self.title2,
            name="Podiobooks Title #2 Episode #2",
            sequence=2,
            description="This is the second wonderful episode of the test title2!",
            url="http://www.Podiobooks.com",
            filesize=32886,
        )

        self.episode4 = Episode.objects.create(
            title=self.title3,
            name="Podiobooks Title #3 Episode #1",
            sequence=1,
            description="This is the first wonderful episode of the test title3!",
            url="http://www.Podiobooks.com",
            filesize=32886,
        )

        # Categories
        self.category1 = Category.objects.create(
            slug='science-fiction',
            name='Science Fiction',
            deleted=False
        )
        TitleCategory.objects.create(title=self.title1, category=self.category1)
        TitleCategory.objects.create(title=self.title2, category=self.category1)

        self.category2 = Category.objects.create(
            slug='fantasy',
            name='Fantasy',
            deleted=False
        )
        TitleCategory.objects.create(title=self.title3, category=self.category1)
        TitleCategory.objects.create(title=self.title3, category=self.category2)

        # Awards
        # @TODO: Add Award-centric test
        self.award1 = Award.objects.create(
            slug='parsec2010',
            name='Parsec Award 2010',
            deleted=False
        )
        self.award1.titles.add(self.title1)
        self.title2.awards.add(self.award1)

        self.award2 = Award.objects.create(
            slug='parsec2010',
            name='Parsec Award 2011',
            deleted=False
        )
        self.award2.titles.add(self.title3)
        self.title3.awards.add(self.award1)  # Title 3 should have two awards now

        # License
        # @TODO: Add License-centric test
        self.license1 = License.objects.create(
            slug='by-nc-nd',
            text='Attribution Noncommercial No Derivatives',
        )
        self.license1.titles.add(self.title1)
        self.title2.license = self.license1

        # Media
        self.media1 = Media.objects.create(
            title=self.title1,
            name='Print Version',
            identifier='3838742922'
        )

        # URLs
        self.url1 = TitleUrl.objects.create(
            title=self.title1,
            url="http://podiobooks.com"
        )

        # Rating
        self.rating = Rating.objects.create(
            last_rating_id=999,
        )

        # Contributors
        self.contributortype1 = ContributorType.objects.create(
            slug='author',
            name='Author',
        )
        self.contributor1 = Contributor.objects.create(
            slug='mur-lafferty',
            first_name='Mur',
            last_name='Lafferty',
            display_name='Mur Lafferty',
            deleted=False
        )
        TitleContributor.objects.create(title=self.title1, contributor_type=self.contributortype1, contributor=self.contributor1)
        TitleContributor.objects.create(title=self.title2, contributor_type=self.contributortype1, contributor=self.contributor1)

        self.contributor2 = Contributor.objects.create(
            slug='nathan-lowell',
            first_name='Nathan',
            last_name='Lowell',
            display_name='Nathan Lowell',
            deleted=False
        )
        TitleContributor.objects.create(title=self.title3, contributor_type=self.contributortype1, contributor=self.contributor1)
        TitleContributor.objects.create(title=self.title3, contributor_type=self.contributortype1, contributor=self.contributor2)  # Title 3 should belong to two contributors now

    def test_series(self):
        """Assert that we creates series correctly, and can access titles from series."""
        for currentSeries in Series.objects.all().filter(name__startswith='Podiobooks Series'):
            # Series Assertions
            if currentSeries.name == "Podiobooks Series #1":
                self.assertEquals(len(currentSeries.titles.all()), 2)
            elif currentSeries.name == "Podiobooks Series #2":
                self.assertEquals(len(currentSeries.titles.all()), 1)
            else:
                self.fail('Non-matching Series!' + currentSeries.name)

    def test_titles(self):
        """Assert that we created titles correctly, and can access everything from titles."""
        #        print '\n---Titles---'
        for currentTitle in Title.objects.all().filter(name__startswith='Podiobooks Title'):
            # Title Assertions
            if currentTitle.name == "Podiobooks Title #1":
                self.assertEquals(len(currentTitle.episodes.all()), 1)
            elif currentTitle.name == "Podiobooks Title #2":
                self.assertEquals(len(currentTitle.episodes.all()), 2)
            elif currentTitle.name == "Podiobooks Title #3":
                self.assertEquals(len(currentTitle.episodes.all()), 1)
            else:
                self.fail('Non-matching Title!' + currentTitle.name)

    def test_categories(self):
        """Assert that we created Categories correctly, and can access titles from categories."""
        #        print '\n---Categories---'
        for currentCategory in Category.objects.all():

            # Category Assertions
            if currentCategory.slug == "science-fiction":
                self.assertEquals(len(currentCategory.title_set.all()), 3)
            elif currentCategory.slug == "fantasy":
                self.assertEquals(len(currentCategory.title_set.all()), 1)
            else:
                self.fail('Non-matching Category!' + currentCategory.name)

        # Count Titles By Category
        category_title_count = Category.objects.aggregate(title_count=Count('title'))  # Counts the main_title_category table
        self.assertEquals(len(category_title_count), 1)

        category_title_group_counts = Category.objects.annotate(title_count=Count('title'))
        self.assertEquals(len(category_title_group_counts), 2)

        category_title_group_counts_filtered = category_title_group_counts.filter(title_count__gt=1)
        self.assertEquals(len(category_title_group_counts_filtered), 1)

        category_title_group_counts_filtered_subset = category_title_group_counts.filter(title_count__gt=1).values_list('slug', 'name')
        self.assertEquals(len(category_title_group_counts_filtered_subset), 1)

        title3 = Title.objects.get(name='Podiobooks Title #3')
        self.assertEquals(len(title3.categories.all()), 2)

    def test_contributors(self):
        """Assert that we created Categories correctly, and can access titles from categories."""
        for currentContributor in Contributor.objects.all():

            # Contributor Assertions
            if currentContributor.slug == "mur-lafferty":
                self.assertEquals(len(currentContributor.title_set.all()), 3)
            elif currentContributor.slug == "nathan-lowell":
                self.assertEquals(len(currentContributor.title_set.all()), 1)
            else:
                self.fail('Non-matching Contributor!' + currentContributor.user.username)

        # Count Titles By Contributor
        contributor_title_count = Contributor.objects.aggregate(title_count=Count('title'))  # Counts the main_title_contributor table
        self.assertEquals(len(contributor_title_count), 1)

        contributor_title_group_counts = Contributor.objects.annotate(title_count=Count('title'))
        self.assertEquals(len(contributor_title_group_counts), 2)

        contributor_title_group_counts_filtered = contributor_title_group_counts.filter(title_count__gt=1)
        self.assertEquals(len(contributor_title_group_counts_filtered), 1)

        contributor_title_group_counts_filtered_subset = contributor_title_group_counts.filter(title_count__gt=1).values_list('slug', 'display_name')
        self.assertEquals(len(contributor_title_group_counts_filtered_subset), 1)

        title3 = Title.objects.get(name='Podiobooks Title #3')
        #        print ('\n\t' + title3.name + ":")
        #        title3contributors = title3.contributors.all()
        #        for currentContributor in title3contributors:
        #            print '\t\tContributor Name: %s' % currentContributor.display_name
        self.assertEquals(len(title3.contributors.all()), 2)

    #    def test_max_rating(self):
    #        """Assert that we can capture the last loaded rating from the PB1 Site."""
    #        print '\n---Max Rating---'
    #        print "\t\tLast Rating Loaded: %s" % self.rating

    def test_media(self):
        """Test pulling Particular Media Items"""
        # http://www.amazon.com/dp/0312384378/?tag=podiobookscom-20
        self.assertEquals(len(self.title1.media.all()), 1)
        print_version = self.title1.media.all().filter(name="Print Version").get()
        self.assertEquals(print_version.identifier, "3838742922")

