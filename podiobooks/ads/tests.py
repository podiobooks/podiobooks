"""Automated unitests for the Podiobooks ad classes"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase
from .models import AdSchedule, AdSchedulePosition, AdScheduleTitle
from podiobooks.core.models import Episode, Title
from django.template.defaultfilters import slugify


class TitleTestCase(TestCase):
    fixtures = ['test_data.json', ]

    def setUp(self):
        # This method sets up a whole series of model objects, and then tries to connect them together.

        # Create an AdSchedule
        self.schedule1 = AdSchedule.objects.create(
            name="Podiobooks Ad Schedule #1",
            description="Test Ad Schedule"
        )

        # Grab Episodes to Attach
        all_episodes = Episode.objects.filter(title__pk=92)
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

        self.title1 = Title.objects.all()[1]

        self.ad_schedule_title = AdScheduleTitle.objects.create(
            title=self.title1,
            ad_schedule=self.schedule1
        )

    def test_ad_schedules(self):
        self.assertEquals(3, self.schedule1.ad_schedule_positions.count())

        self.assertEquals(1, self.title1.ad_schedules.count())

        #  Insert ad episodes into episode list
        episode_list = list(self.title1.episodes.all())
        ad_schedule_positions = AdSchedulePosition.objects.filter(ad_schedule__in=self.title1.ad_schedules.all())
        for position in ad_schedule_positions:
            episode_list.insert(position.sequence - 1, position.episode)  # sequence - 1 since .insert inserts after

        print episode_list
        self.assertEquals(self.episode1, episode_list[4])
        self.assertEquals(26, len(episode_list))

    def test_multiple_ad_schedules(self):
        # Create a Second AdSchedule
        schedule2 = AdSchedule.objects.create(
            name="Podiobooks Ad Schedule #2",
            description="Test Ad Schedule 2",
            priority=30
        )

        # Grab Episodes to Attach
        all_episodes = Episode.objects.filter(title__pk=250)
        episode2_1 = all_episodes[1]
        episode2_2 = all_episodes[2]

        # Add Ad Episodes to AdSchedule
        ad_schedule_ep1 = AdSchedulePosition.objects.create(
            ad_schedule=schedule2,
            episode=episode2_1,
            sequence=5
        )

        ad_schedule_ep2 = AdSchedulePosition.objects.create(
            ad_schedule=schedule2,
            episode=episode2_2,
            sequence=15
        )

        self.ad_schedule_title = AdScheduleTitle.objects.create(
            title=self.title1,
            ad_schedule=schedule2
        )

        self.assertEquals(2, schedule2.ad_schedule_positions.count())
        self.assertEquals(2, self.title1.ad_schedules.count())

        #  Insert ad episodes into episode list
        episode_list = list(self.title1.episodes.all())
        ad_schedule_positions = AdSchedulePosition.objects.filter(ad_schedule__in=self.title1.ad_schedules.all())
        for position in ad_schedule_positions:
            episode_list.insert(position.sequence - 1, position.episode)  # sequence - 1 since .insert inserts after

        print episode_list
        self.assertEquals(episode2_1, episode_list[4])
        self.assertEquals(28, len(episode_list))
