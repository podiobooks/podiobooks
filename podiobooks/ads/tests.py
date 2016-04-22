"""Automated unitests for the Podiobooks ad classes"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase
from .models import AdSchedule, AdSchedulePosition
from podiobooks.core.models import Episode, Title
from .models import get_active_ad_scheds_for_title, get_ep_list_with_ads_for_title
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone


class AdScheduleTestCase(TestCase):
    fixtures = ['test_data.json', ]

    def setUp(self):
        # This method sets up a whole series of model objects, and then tries to connect them together.

        # Create an AdSchedule
        self.schedule1 = AdSchedule.objects.create(
            name="Podiobooks Ad Schedule #1",
            description="Test Ad Schedule",
            date_start=datetime.datetime(2013, 1, 1, 0, 0, 0, 0, timezone.utc),
            date_end=datetime.datetime.now(timezone.utc) + datetime.timedelta(10)
        )

        # Grab Episodes to Attach
        all_episodes = Episode.objects.filter(title__slug='pb-ads')
        self.episode1 = all_episodes[1]
        self.episode2 = all_episodes[2]

        # Add Ad Episodes to AdSchedule
        self.ad_schedule_ep1 = AdSchedulePosition.objects.create(
            ad_schedule=self.schedule1,
            episode=self.episode1,
            sequence=5
        )

        self.ad_schedule_ep2 = AdSchedulePosition.objects.create(
            ad_schedule=self.schedule1,
            episode=self.episode2,
            sequence=10
        )

        self.ad_schedule_ep2 = AdSchedulePosition.objects.create(
            ad_schedule=self.schedule1,
            episode=self.episode1,
            sequence=15
        )

        self.schedule2 = AdSchedule.objects.create(
            name="Podiobooks Ad Schedule #2",
            description="Test Ad Schedule 2",
            priority=30,
            date_start=datetime.datetime(2012, 1, 1, 0, 0, 0, 0, timezone.utc),
            date_end=datetime.datetime.now(timezone.utc) + datetime.timedelta(10)
        )

        # Grab Episodes to Attach
        all_episodes = Episode.objects.filter(title__pk=250)
        self.episode2_1 = all_episodes[1]
        self.episode2_2 = all_episodes[2]

        # Add Ad Episodes to AdSchedule
        ad_schedule_ep1 = AdSchedulePosition.objects.create(
            ad_schedule=self.schedule2,
            episode=self.episode2_1,
            sequence=5
        )

        ad_schedule_ep2 = AdSchedulePosition.objects.create(
            ad_schedule=self.schedule2,
            episode=self.episode2_2,
            sequence=15
        )

        self.title1 = Title.objects.get(slug='earthcore')

        self.schedule1.titles.add(self.title1)
        # Not adding schedule2 to title till specific test cases

    def test_with_no_ad_schedules(self):
        self.schedule1.titles.remove(self.title1)
        self.assertEquals(3, self.schedule1.ad_schedule_positions.count())
        self.assertEquals(0, get_active_ad_scheds_for_title(self.title1).count())

        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list

        self.assertEquals(self.title1.episodes.all()[4], episode_list[4])
        self.assertEquals(23, len(episode_list))

    def test_ad_schedules(self):
        self.assertEquals(3, self.schedule1.ad_schedule_positions.count())
        self.assertEquals(1, get_active_ad_scheds_for_title(self.title1).count())

        #  Insert ad episodes into episode list
        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list

        self.assertEquals(self.episode1, episode_list[4])
        self.assertEquals(26, len(episode_list))

    def test_multiple_ad_schedules(self):
        self.schedule2.titles.add(self.title1)

        self.assertEquals(2, self.schedule2.ad_schedule_positions.count())
        self.assertEquals(2, get_active_ad_scheds_for_title(self.title1).count())

        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list

        self.assertEquals(self.episode2_1, episode_list[4])
        self.assertEquals(28, len(episode_list))

    def test_future_ad_schedules(self):
        self.schedule2.titles.add(self.title1)
        self.schedule2.date_start = datetime.datetime.now(timezone.utc) + datetime.timedelta(5)  # Expire 5 days in future
        self.schedule2.save()

        self.assertEquals(1, get_active_ad_scheds_for_title(self.title1).count())

        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list

        self.assertEquals(self.episode1, episode_list[4])
        self.assertEquals(26, len(episode_list))

    def test_expired_ad_schedules(self):
        self.schedule2.titles.add(self.title1)
        self.schedule2.date_end = datetime.datetime.now(timezone.utc) - datetime.timedelta(5)  # Expire 5 days in past
        self.schedule2.save()

        self.assertEquals(2, self.schedule2.ad_schedule_positions.count())
        self.assertEquals(1, get_active_ad_scheds_for_title(self.title1).count())

        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list

        self.assertEquals(self.episode1, episode_list[4])
        self.assertEquals(26, len(episode_list))

        # Test no active ad schedules
        self.schedule1.date_end = datetime.datetime.now(timezone.utc) - datetime.timedelta(5)  # Expire 5 days in past
        self.schedule1.save()

        self.assertEquals(0, get_active_ad_scheds_for_title(self.title1).count())
        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list

        self.assertEquals(self.title1.episodes.all()[4], episode_list[4])
        self.assertEquals(23, len(episode_list))

    def test_shared_ad_schedules(self):
        self.title2 = Title.objects.get(slug='the-plump-buffet')
        self.schedule1.titles.add(self.title2)

        self.assertEquals(3, self.schedule1.ad_schedule_positions.count())
        self.assertEquals(2, self.schedule1.titles.count())
        self.assertEquals(1, get_active_ad_scheds_for_title(self.title1).count())
        self.assertEquals(1, get_active_ad_scheds_for_title(self.title2).count())

        episode_list = get_ep_list_with_ads_for_title(self.title2)
        # print episode_list
        self.assertEquals(self.episode1, episode_list[4])

    def test_end_of_title_ad(self):
        self.ad_schedule_ep99 = AdSchedulePosition.objects.create(
            ad_schedule=self.schedule1,
            episode=self.episode1,
            sequence=99
        )

        episode_list = get_ep_list_with_ads_for_title(self.title1)
        # print episode_list
        # print len(episode_list)
        self.assertEquals(self.episode1, episode_list[len(episode_list)-1])

