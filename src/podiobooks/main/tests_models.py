from django.test import TestCase
from podiobooks.main.models import *  #@UnusedWildImport
from django.template.defaultfilters import slugify
from django.test.client import Client

class TitleTestCase(TestCase):
    fixtures = []
    
    def setUp(self):
        # This method sets up a whole series of model objects, and then tries to connect them together.
        
        #Create Some Test Users
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', 'testuser2password')
        self.user3 = User.objects.create_user('testuser3', 'testuser3@test.com', 'testuser3password')
        
        self.user1.first_name = "test1"
        self.user1.last_name = "user1"
        self.user1.save
        
        self.user2.first_name = "test2"
        self.user2.last_name = "user2"
        self.user2.save
        
        self.user3.first_name = "test3"
        self.user3.last_name = "user3"
        self.user3.save
        
        # Create some UserProfiles for those test users
        self.user1profile = UserProfile.objects.create (
            user = self.user1,
            slug = slugify(self.user1.get_full_name())
            )
        
        self.user2profile = UserProfile.objects.create (
            user = self.user2,
            slug = slugify(self.user2.get_full_name())
            )
        
        self.user3profile = UserProfile.objects.create (
            user = self.user3,
            slug = slugify(self.user3.get_full_name())
            )
        
        # Create Some Series
        self.series1 = Series.objects.create (
            name = "Podiobooks Series #1",
            description = "A wonderful sample series that contains many fine books",
            url = "http://www.Podiobooks.com",
            deleted = False
            )
        self.series1.slug = slugify(self.series1.name)
        
        self.series2 = Series.objects.create (
            name = "Podiobooks Series #2",
            description = "Another wonderful sample series that contains many fine books",
            url = "http://www.Podiobooks.com",
            deleted = False
            )
        self.series2.slug = slugify(self.series2.name)
        
        # Create Some Titles
        self.title1 = Title.objects.create (
                name = "Podiobooks Title #1",
                slug = slugify("Podiobooks Title #1"),
                series = self.series1,
                description = "A fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
                cover = "PodioBook Cover",
                status = 1,
                display_on_homepage = True,
                is_hosted_at_pb = True,
                is_adult = False,
                is_complete = False,
                avg_audio_quality = 4.5,
                avg_narration = 3.5,
                avg_writing = 2.5,
                avg_overall = 3.75,
                deleted = False
                )
        
        self.title2 = Title.objects.create (
                name = "Podiobooks Title #2",
                slug = slugify("Podiobooks Title #2"),
                series = self.series1,
                description = "A second fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
                cover = "PodioBook Cover 2",
                status = 1,
                display_on_homepage = True,
                is_hosted_at_pb = True,
                is_adult = False,
                is_complete = False,
                avg_audio_quality = 3.5,
                avg_narration = 4.5,
                avg_writing = 5.5,
                avg_overall = 6.75,
                deleted = False
                )
        
        self.title3 = Title.objects.create (
                name = "Podiobooks Title #3",
                slug = slugify("Podiobooks Title #3"),
                series = self.series2,
                description = "A third fantastic sample book of surpassing quality and scope, that truly redefines what it means to be a PodioBook.",
                cover = "PodioBook Cover 3",
                status = 1,
                display_on_homepage = True,
                is_hosted_at_pb = True,
                is_adult = False,
                is_complete = False,
                avg_audio_quality = 1.5,
                avg_narration = 2.5,
                avg_writing = 3.5,
                avg_overall = 4.75,
                deleted = False
                )
        
        #Create a Partner Object
        self.partner1 = Partner.objects.create (
            name = "Podiobooks Partner #1",
            url = "http://Podiobooks.com",
            logo = "http://Podiobooks.com",
            deleted = False
            )
        
        #Create some Episodes
        self.episode1 = Episode.objects.create (
            title = self.title1,
            name = "Podiobooks Title #1 Episode #1",
            sequence = 1,
            description = "This is the first wonderful episode of the test title1!",
            url = "http://www.Podiobooks.com",
            filesize = 328886,
            status = 1,
            deleted = False,
            )
        
        self.episode2 = Episode.objects.create (
            title = self.title2,
            name = "Podiobooks Title #2 Episode #1",
            sequence = 1,
            description = "This is the first wonderful episode of the test title2!",
            url = "http://www.Podiobooks.com",
            filesize = 32886,
            status = 1,
            deleted = False,
            )
        
        self.episode3 = Episode.objects.create (
            title = self.title2,
            name = "Podiobooks Title #2 Episode #2",
            sequence = 1,
            description = "This is the second wonderful episode of the test title2!",
            url = "http://www.Podiobooks.com",
            filesize = 32886,
            status = 1,
            deleted = False,
            )
        
        self.episode4 = Episode.objects.create (
            title = self.title3,
            name = "Podiobooks Title #3 Episode #1",
            sequence = 1,
            description = "This is the first wonderful episode of the test title3!",
            url = "http://www.Podiobooks.com",
            filesize = 32886,
            status = 1,
            deleted = False,
            )
        
        # Create Some Subscriptions
        
        # Subscribed to a title and a series case
        self.subscription1 = Subscription.objects.create (
                user = self.user1,
                day_interval = 5,
                partner = self.partner1,
                last_downloaded_episode = self.episode1,
                last_downloaded_date = datetime.datetime.now(),
                finished = False,
                deleted = False
                )
        self.subscription1.titles.add(self.title1)
        self.subscription1.series.add(self.series2)
        
        # Subscribed to two titles case
        self.subscription2 = Subscription.objects.create (
                user = self.user2,
                day_interval = 10,
                partner = self.partner1,
                last_downloaded_episode = self.episode2,
                last_downloaded_date = datetime.datetime.now(),
                finished = False,
                deleted = False
                )
        self.subscription2.titles.add(self.title1)
        self.subscription2.titles.add(self.title2)
        
        # Subscribed to two series case
        self.subscription3 = Subscription.objects.create (
                user = self.user3,
                day_interval = 6,
                partner = self.partner1,
                last_downloaded_episode = self.episode3,
                last_downloaded_date = datetime.datetime.now(),
                finished = False,
                deleted = False
                )
        self.subscription3.series.add(self.series1)
        self.subscription3.series.add(self.series2)     

    def testAll(self):
        # USERS
        print 'Users:'
        testUsers = User.objects.all().filter(username__startswith='test')
        
        for currentUser in testUsers:
            print '\tUsername: %s\tSlug: %s' % (currentUser.username, currentUser.get_profile().slug)
            
        # User Assertions
        self.assertEquals(len(testUsers), 3)
        

        # SERIES
        print '\nSeries: '
        for currentSeries in Series.objects.all().filter(name__startswith='Podiobooks Series') :
            print '\n\tName: %s' % currentSeries.name
            print '\tSlug: %s' % currentSeries.slug
            print '\tTitles:'
            for currentTitle in currentSeries.title_set.all() :
                print '\t\tName: %s' % currentTitle.name
                print '\t\tSlug: %s' % currentTitle.slug
            print '\tSubscriptions:'
            for currentSubscription in currentSeries.subscription_set.all() :
                print '\t\tUserName: %s' % currentSubscription.user.username
            
            # Series Assertions
            if currentSeries.name == "Podiobooks Series #1" :
                self.assertEquals(len(currentSeries.subscription_set.all()), 1)
                self.assertEquals(len(currentSeries.title_set.all()), 2)
            elif currentSeries.name == "Podiobooks Series #2" :
                self.assertEquals(len(currentSeries.subscription_set.all()), 2)
                self.assertEquals(len(currentSeries.title_set.all()), 1)
            else :
                self.fail('Non-matching Series!' + currentSeries.name)
                
        # TITLES 
        print '\nTitles: '
        for currentTitle in Title.objects.all().filter(name__startswith='Podiobooks Title') :
            print '\n\tName: %s' % currentTitle.name
            print '\tSlug: %s' % currentTitle.slug
            print '\tSeries: %s' % currentTitle.series.name
            print '\tEpisodes:'
            for currentEpisode in currentTitle.episode_set.all() :
                print '\t\tName: %s' % currentEpisode.name
            print '\tSubscriptions:'
            for currentSubscription in currentTitle.subscription_set.all() :
                print '\t\tUserName: %s' % currentSubscription.user.username
            
            # Title Assertions
            if currentTitle.name == "Podiobooks Title #1" :
                self.assertEquals(len(currentTitle.episode_set.all()), 1)
                self.assertEquals(len(currentTitle.subscription_set.all()), 2)
            elif currentTitle.name == "Podiobooks Title #2" :
                self.assertEquals(len(currentTitle.episode_set.all()), 2)
                self.assertEquals(len(currentTitle.subscription_set.all()), 1)
            elif currentTitle.name == "Podiobooks Title #3" :
                self.assertEquals(len(currentTitle.episode_set.all()), 1)
                self.assertEquals(len(currentTitle.subscription_set.all()), 0)
            else :
                self.fail('Non-matching Title!' + currentTitle.name)
                
        # SUBSCRIPTIONS  
        print '\nSubscriptions'
        for currentSubscription in Subscription.objects.all() :
            print '\n\tUser: %s:%s' % (currentSubscription.user.username, currentSubscription.user.get_profile().slug)
            print '\tPartner: %s' % currentSubscription.partner.name
            print '\tLast Episode Downloaded: %s' % currentSubscription.last_downloaded_episode.name
            print '\n\tTitles: '
            for currentTitle in currentSubscription.titles.all() :
                print '\t\tName: %s' % currentTitle.name
            print '\n\tSeries: '
            for currentSeries in currentSubscription.series.all() :
                print '\t\tName: %s' % currentSeries.name
                
            # Subscription Assertions
            if currentSubscription.user.username == "testuser1" :
                self.assertEquals(len(currentSubscription.titles.all()), 1)
                self.assertEquals(len(currentSubscription.series.all()), 1)
                self.assertEquals("test1-user1", currentSubscription.user.get_profile().slug)
            elif currentSubscription.user.username == "testuser2" :
                self.assertEquals(len(currentSubscription.titles.all()), 2)
                self.assertEquals(len(currentSubscription.series.all()), 0)
                self.assertEquals("test2-user2", currentSubscription.user.get_profile().slug)
            elif currentSubscription.user.username == "testuser3" :
                self.assertEquals(len(currentSubscription.titles.all()), 0)
                self.assertEquals(len(currentSubscription.series.all()), 2)
                self.assertEquals("test3-user3", currentSubscription.user.get_profile().slug)
            else :
                self.fail('Non-matching Subscription!' + currentSubscription.user.username)

class UrlTestCase(TestCase):
    fixtures = []
    
    def testAll(self):
        c = Client() # create a new test client
        response = c.get('/')
        self.assertEquals(200, response.status_code)
