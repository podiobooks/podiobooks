"""Automated unitests for the Podiobooks model classes"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase
from podiobooks.core.models import *  #@UnusedWildImport
from django.template.defaultfilters import slugify
from django.db.models import Count

class TitleTestCase(TestCase):
    """Test the Podiobooks Models from a Title-Centric POV"""
    
    def setUp(self):
        
        # This method sets up a whole series of model objects, and then tries to connect them together.
        
        #Create Some Test Users
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', 'testuser2password')
        self.user3 = User.objects.create_user('testuser3', 'testuser3@test.com', 'testuser3password')
        
        self.user1.first_name = "test1"
        self.user1.last_name = "user1"
        user1Profile = self.user1.get_profile()
        user1Profile.slug = slugify(self.user1.get_full_name())
        user1Profile.save()
        
        self.user2.first_name = "test2"
        self.user2.last_name = "user2"
        user2Profile = self.user2.get_profile()
        user2Profile.slug = slugify(self.user2.get_full_name())
        user2Profile.save()
        
        self.user3.first_name = "test3"
        self.user3.last_name = "user3"
        user3Profile = self.user3.get_profile()
        user3Profile.slug = slugify(self.user3.get_full_name())
        user3Profile.save()
        
        # Create Some Series
        self.series1 = Series.objects.create (
            name="Podiobooks Series #1",
            description="A wonderful sample series that contains many fine books",
            url="http://www.Podiobooks.com",
            )
        self.series1.slug = slugify(self.series1.name)
        self.series1.save()
        
        self.series2 = Series.objects.create (
            name="Podiobooks Series #2",
            description="Another wonderful sample series that contains many fine books",
            url="http://www.Podiobooks.com",
            )
        self.series2.slug = slugify(self.series2.name)
        self.series2.save()
        
        # Create Some Titles
        self.title1 = Title.objects.create (
                name="Podiobooks Title #1",
                slug=slugify("Podiobooks Title #1"),
                series=self.series1,
                description="A fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
                cover="PodioBook Cover",
                status=1,
                display_on_homepage=True,
                is_hosted_at_pb=True,
                is_adult=False,
                is_explicit=True,
                is_complete=False,
                avg_audio_quality=4.5,
                avg_narration=3.5,
                avg_writing=2.5,
                avg_overall=3.75,
                promoter_count=211,
                detractor_count=100,
                )
        
        self.title2 = Title.objects.create (
                name="Podiobooks Title #2",
                slug=slugify("Podiobooks Title #2"),
                series=self.series1,
                description="A second fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
                cover="PodioBook Cover 2",
                status=1,
                display_on_homepage=True,
                is_hosted_at_pb=True,
                is_adult=False,
                is_explicit=False,
                is_complete=False,
                avg_audio_quality=3.5,
                avg_narration=4.5,
                avg_writing=5.5,
                avg_overall=6.75,
                )
        
        self.title3 = Title.objects.create (
                name="Podiobooks Title #3",
                slug=slugify("Podiobooks Title #3"),
                series=self.series2,
                description="A third fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
                cover="PodioBook Cover 3",
                status=1,
                display_on_homepage=True,
                is_hosted_at_pb=True,
                is_adult=False,
                is_explicit=False,
                is_complete=False,
                avg_audio_quality=1.5,
                avg_narration=2.5,
                avg_writing=3.5,
                avg_overall=4.75,
                )
        
        #Create a Partner Object
        self.partner1 = Partner.objects.create (
            name="Podiobooks Partner #1",
            url="http://Podiobooks.com",
            logo="http://Podiobooks.com",
            )
        
        #Create some Episodes
        self.episode1 = Episode.objects.create (
            title=self.title1,
            name="Podiobooks Title #1 Episode #1",
            sequence=1,
            description="This is the first wonderful episode of the test title1!",
            url="http://www.Podiobooks.com",
            filesize=328886,
            )
        
        self.episode2 = Episode.objects.create (
            title=self.title2,
            name="Podiobooks Title #2 Episode #1",
            sequence=1,
            description="This is the first wonderful episode of the test title2!",
            url="http://www.Podiobooks.com",
            filesize=32886,
            )
        
        self.episode3 = Episode.objects.create (
            title=self.title2,
            name="Podiobooks Title #2 Episode #2",
            sequence=2,
            description="This is the second wonderful episode of the test title2!",
            url="http://www.Podiobooks.com",
            filesize=32886,
            )
        
        self.episode4 = Episode.objects.create (
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
        self.title3.awards.add(self.award1) #Title 3 should have two awards now
        
        # Advisories
        # @TODO: Add Advisory-centric test
        self.advisory1 = Advisory.objects.create(
                slug='advisory-test-1',
                name='Advisory Test 1',
                )
        self.advisory1.titles.add(self.title1)
        self.title2.advisory = self.advisory1
        
        self.advisory2 = Award.objects.create(
                slug='advisory-test-2',
                name='Advisory Test 2',
                )
        self.advisory2.titles.add(self.title3)
        
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
                name='Smashwords Version',
                )
        
        # Partner
        # @TODO: Add Partner-centric test
        self.partner1 = Partner.objects.create(
                name='Audible',
                url="http://audible.com"
        )
        self.title1.partner = self.partner1
        self.partner1.titles.add(self.title2)
        
        # Promo
        self.promo1 = Promo.objects.create(
                title=self.title1,
                name='Promo 1',
                url="http://podiobooks.com"
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
        TitleContributor.objects.create(title=self.title3, contributor_type=self.contributortype1, contributor=self.contributor2) #Title 3 should belong to two contributors now

    def test_users(self):
        """Assert that we created users correctly."""
        print '---Users---'
        testUsers = User.objects.all().filter(username__startswith='test')
        
        for currentUser in testUsers:
            print '\tUsername: %s\tSlug: %s' % (currentUser.username, currentUser.get_profile().slug)
        # User Assertions
        self.assertEquals(len(testUsers), 3)

    def test_series(self):
        """Assert that we creates series correctly, and can access titles from series."""
        print '\n---Series---'
        for currentSeries in Series.objects.all().filter(name__startswith='Podiobooks Series') :
            print '\n\tName: %s' % currentSeries
            print '\tSlug: %s' % currentSeries.slug
            print '\tURL: %s' % currentSeries.get_absolute_url()
            print '\tTitles:'
            for currentTitle in currentSeries.titles.all() :
                print '\t\tName: %s' % currentTitle.name
                print '\t\tSlug: %s' % currentTitle.slug
                print '\tURL: %s' % currentTitle.get_absolute_url()
                print '\tNet Promoter Score: %s' % currentTitle.net_promoter_score()
                print '\tDesc With <br>: %s' % currentTitle.description_br()
            
            # Series Assertions
            if currentSeries.name == "Podiobooks Series #1" :
                self.assertEquals(len(currentSeries.titles.all()), 2)
            elif currentSeries.name == "Podiobooks Series #2" :
                self.assertEquals(len(currentSeries.titles.all()), 1)
            else :
                self.fail('Non-matching Series!' + currentSeries.name)
                
    def test_titles(self):
        """Assert that we created titles correctly, and can access everything from titles.""" 
        print '\n---Titles---'
        for currentTitle in Title.objects.all().filter( name__startswith='Podiobooks Title' ) :
            print '\n\tName: %s' % currentTitle
            print '\tSlug: %s' % currentTitle.slug
            print '\tSeries: %s' % currentTitle.series.name
            print '\tEpisodes:'
            for currentEpisode in currentTitle.episodes.all() :
                print '\t\tName: %s - %s - %s' % ( currentEpisode, currentEpisode.get_absolute_url(), currentEpisode.filesize_mb )
            print '\tCategories:'
            for currentCategory in currentTitle.categories.all() :
                print '\t\t%s - url: %s' % ( currentCategory, currentCategory.get_absolute_url() )
            print '\tAwards:'
            for currentAward in currentTitle.awards.all() :
                print '\t\t%s' % ( currentAward )
            print '\tContributors:'
            for currentTitleContributor in currentTitle.titlecontributors.all() :
                print '\t\t%s (%s) - %s' % ( currentTitleContributor.contributor, currentTitleContributor.contributor_type, currentTitleContributor.contributor.get_absolute_url() )
            if currentTitle.advisory:
                print '\tAdvisory: %s' % currentTitle.advisory
            if currentTitle.license:
                print '\tLicense: %s' % currentTitle.license
            if currentTitle.partner:
                print '\tPartner: %s' % currentTitle.partner
            if currentTitle.media:
                for currentMedia in currentTitle.media.all() :
                    print '\tMedia: %s' % currentMedia
            if currentTitle.promos:
                for currentPromo in currentTitle.promos.all() :
                    print '\tPromo: %s' % currentPromo
            if currentTitle.urls:
                for currentURL in currentTitle.urls.all() :
                    print '\tURL: %s' % currentURL
            
            # Title Assertions
            if currentTitle.name == "Podiobooks Title #1" :
                self.assertEquals( len( currentTitle.episodes.all() ), 1 )
            elif currentTitle.name == "Podiobooks Title #2" :
                self.assertEquals(len(currentTitle.episodes.all()), 2)
            elif currentTitle.name == "Podiobooks Title #3" :
                self.assertEquals(len(currentTitle.episodes.all()), 1)
            else :
                self.fail('Non-matching Title!' + currentTitle.name)
                     
    def test_categories(self):
        """Assert that we created Categories correctly, and can access titles from categories."""
        print '\n---Categories---'
        for currentCategory in Category.objects.all() :
            print '\n\tSlug/Name: %s/%s' % (currentCategory.slug, currentCategory.name)
            for currentTitle in currentCategory.title_set.all() :
                print '\t\tName: %s' % currentTitle.name
                
            # Category Assertions
            if currentCategory.slug == "science-fiction" :
                self.assertEquals(len(currentCategory.title_set.all()), 3)
            elif currentCategory.slug == "fantasy" :
                self.assertEquals(len(currentCategory.title_set.all()), 1)
            else :
                self.fail('Non-matching Category!' + currentCategory.name)
                
        # Count Titles By Category
        categoryTitleCount = Category.objects.aggregate(title_count=Count('title')) # Counts the main_title_category table
        print '\n\tTitle/Category Count: ' + str(categoryTitleCount['title_count'])
        self.assertEquals(len(categoryTitleCount), 1)
        
        categoryTitleGroupCounts = Category.objects.annotate(title_count=Count('title'))
        print  '\n\tTitle Counts by Category:\n',
        for categoryTitleGroup in categoryTitleGroupCounts:
            print  '\t\t%s: %d' % (categoryTitleGroup.name, categoryTitleGroup.title_count)
        self.assertEquals(len(categoryTitleGroupCounts), 2)
            
        categoryTitleGroupCountsFiltered = categoryTitleGroupCounts.filter(title_count__gt=1)
        print  '\n\tFiltered Title Counts by Category:\n',
        for categoryTitleGroup in categoryTitleGroupCountsFiltered:
            print  '\t\t%s: %d' % (categoryTitleGroup.name, categoryTitleGroup.title_count)
        self.assertEquals(len(categoryTitleGroupCountsFiltered), 1)
        
        categoryTitleGroupCountsFilteredSubset = categoryTitleGroupCounts.filter(title_count__gt=1).values_list('slug','name')
        print  '\n\tField Subset of Filtered Categories:\n',
        for categorySubset in categoryTitleGroupCountsFilteredSubset:
            print  '\t\t%s/%s' % (categorySubset[0], categorySubset[1])
        self.assertEquals(len(categoryTitleGroupCountsFilteredSubset), 1)
            
        title3 = Title.objects.get(name='Podiobooks Title #3')
        print ('\n\t' + title3.name + ":")
        for currentCategory in title3.categories.all() :
            print '\t\tCategory Name: %s' % currentCategory.name
        self.assertEquals(len(title3.categories.all()), 2)
        
    def test_contributors(self):
        """Assert that we created Categories correctly, and can access titles from categories.""" 
        print '\n---Contributors---'
        for currentContributor in Contributor.objects.all() :
            print '\n\tSlug/Name: %s/%s' % (currentContributor.slug, currentContributor.display_name)
            for currentTitle in currentContributor.title_set.all() :
                print '\t\tName: %s' % currentTitle.name
                
            # Contributor Assertions
            if currentContributor.slug == "mur-lafferty" :
                self.assertEquals(len(currentContributor.title_set.all()), 3)
            elif currentContributor.slug == "nathan-lowell" :
                self.assertEquals(len(currentContributor.title_set.all()), 1)
            else :
                self.fail('Non-matching Contributor!' + currentContributor.user.username)
                
        # Count Titles By Contributor
        contributorTitleCount = Contributor.objects.aggregate(title_count=Count('title')) # Counts the main_title_contributor table
        print '\n\tTitle/Contributor Count: ' + str(contributorTitleCount['title_count'])
        self.assertEquals(len(contributorTitleCount), 1)
        
        contributorTitleGroupCounts = Contributor.objects.annotate(title_count=Count('title'))
        print  '\n\tTitle Counts by Contributor:\n',
        for contributorTitleGroup in contributorTitleGroupCounts:
            print  '\t\t%s: %d' % (contributorTitleGroup.display_name, contributorTitleGroup.title_count)
        self.assertEquals(len(contributorTitleGroupCounts), 2)
            
        contributorTitleGroupCountsFiltered = contributorTitleGroupCounts.filter(title_count__gt=1)
        print  '\n\tFiltered Title Counts by Contributor:\n',
        for contributorTitleGroup in contributorTitleGroupCountsFiltered:
            print  '\t\t%s: %d' % (contributorTitleGroup.display_name, contributorTitleGroup.title_count)
        self.assertEquals(len(contributorTitleGroupCountsFiltered), 1)
        
        contributorTitleGroupCountsFilteredSubset = contributorTitleGroupCounts.filter(title_count__gt=1).values_list('slug','display_name')
        print  '\n\tField Subset of Filtered Contributors:\n',
        for contributorSubset in contributorTitleGroupCountsFilteredSubset:
            print  '\t\t%s/%s' % (contributorSubset[0], contributorSubset[1])
        self.assertEquals(len(contributorTitleGroupCountsFilteredSubset), 1)
        
        title3 = Title.objects.get(name='Podiobooks Title #3')
        print ('\n\t' + title3.name + ":")
        title3contributors = title3.contributors.all() 
        for currentContributor in title3contributors:
            print '\t\tContributor Name: %s' % currentContributor.display_name
        self.assertEquals(len(title3.contributors.all()), 2)
        
    def test_bylines(self):
        """Assert that the creation of bylines is working."""
        print '\n---Bylines---'
        title3titlecontributors = self.title3.titlecontributors.all().order_by('contributor_type__slug', 'date_created')
        bylineFromTemplate = render_to_string('core/title/tags/show_contributors.html', {'titlecontributors': title3titlecontributors,})
        
        print "\t\tTemplate Byline: %s" % bylineFromTemplate
        print "\t\tAuto Byline: %s" % self.title3.byline
        self.assertEquals(bylineFromTemplate.strip(), self.title3.byline)
    
    def test_max_rating(self):
        """Assert that we can capture the last loaded rating from the PB1 Site."""
        print '\n---Max Rating---'
        print "\t\tLast Rating Loaded: %s" % self.rating

