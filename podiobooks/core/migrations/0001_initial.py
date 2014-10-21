# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(blank=True)),
                ('image', models.ImageField(max_length=255, upload_to=b'images/awards')),
                ('deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=50)),
                ('deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=1000)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255, blank=True)),
                ('last_name', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=1024, blank=True)),
                ('community_handle', models.CharField(max_length=255, blank=True)),
                ('scribl_username', models.CharField(max_length=255, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name=b'contributor_info', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContributorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('byline_text', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Contributor Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('sequence', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField()),
                ('filesize', models.IntegerField(default=0, help_text=b"In bytes, corresponds to 'length' in RSS feed")),
                ('duration', models.CharField(default=b'45:00', help_text=b'Duration of the media file in minutes:seconds', max_length=20)),
                ('deleted', models.BooleanField(default=False, db_index=True)),
                ('media_date_created', models.DateTimeField(help_text=b'Date the media file was added (e.g. to Libsyn)', null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title__name', 'sequence'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EpisodeContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('contributor', models.ForeignKey(related_name=b'episodecontributors', to='core.Contributor')),
                ('contributor_type', models.ForeignKey(related_name=b'episodecontributors', to='core.ContributorType')),
                ('episode', models.ForeignKey(related_name=b'episodecontributors', to='core.Episode')),
            ],
            options={
                'verbose_name_plural': 'Episode Contributors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('text', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('image_url', models.URLField()),
                ('code', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Print Version', max_length=255, choices=[(b'Print Version', b'Print Version'), (b'Kindle Version', b'Kindle Version'), (b'Smashwords Version', b'Smashwords Version')])),
                ('identifier', models.CharField(help_text=b'ISBN or Product ID', max_length=255, blank=True)),
                ('url', models.CharField(max_length=255, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'media',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_rating_id', models.IntegerField(default=0, db_index=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'date_created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'series',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assets_from_images', models.TextField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('series_sequence', models.IntegerField(default=1, verbose_name=b'Series Sequence')),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('old_slug', models.SlugField(max_length=255, unique=True, null=True, blank=True)),
                ('cover', models.ImageField(max_length=500, null=True, upload_to=b'images/covers', blank=True)),
                ('display_on_homepage', models.BooleanField(default=False, db_index=True, verbose_name=b'Disp. On Homepage')),
                ('is_adult', models.BooleanField(default=False, db_index=True, verbose_name=b'Is Adult')),
                ('is_explicit', models.BooleanField(default=False, db_index=True, verbose_name=b'Is Explicit')),
                ('is_family_friendly', models.BooleanField(default=False, db_index=True, verbose_name=b'Is Family Friendly')),
                ('is_for_kids', models.BooleanField(default=False, db_index=True, verbose_name=b'Is For Kids')),
                ('language', models.CharField(default=b'en-us', help_text=b'Language Code for Title', max_length=10, db_index=True)),
                ('promoter_count', models.IntegerField(default=0, db_index=True)),
                ('detractor_count', models.IntegerField(default=0, db_index=True)),
                ('deleted', models.BooleanField(default=False, db_index=True, verbose_name=b'Deleted?')),
                ('byline', models.CharField(max_length=1024, blank=True)),
                ('category_list', models.CharField(max_length=1024, blank=True)),
                ('payment_email_address', models.EmailField(help_text=b'Email address to send payments or tips for this title.', max_length=75, null=True, blank=True)),
                ('libsyn_show_id', models.CharField(help_text=b'Starts with k-', max_length=50, verbose_name=b'LibSyn Show ID', db_index=True, blank=True)),
                ('libsyn_slug', models.SlugField(help_text=b'Show Slug from Libsyn', verbose_name=b'LibSyn Slug', blank=True)),
                ('libsyn_cover_image_url', models.URLField(help_text=b'Full URL to Libsyn-hosted cover image.', max_length=500, null=True, verbose_name=b'Libsyn Cover Image URL', blank=True)),
                ('itunes_adam_id', models.IntegerField(help_text=b'From iTunes Page URL for Podcast', null=True, verbose_name=b'iTunes ADAM Id', blank=True)),
                ('itunes_new_feed_url', models.BooleanField(default=False, help_text=b'Include <itunes:new_feed_url> tag in feed (Required if you are changing the slug)', verbose_name=b'iTunes New Feed Url Tag')),
                ('podiobooker_blog_url', models.URLField(help_text=b'Full URL to Blog Post Announcing Book - Used to Pull Comments', max_length=255, null=True, verbose_name=b'Blog URL', blank=True)),
                ('scribl_book_id', models.CharField(max_length=20, null=True, verbose_name=b'Scribl Book Id', blank=True)),
                ('tips_allowed', models.BooleanField(default=True, verbose_name=b'Collect Tips for this Title')),
                ('scribl_allowed', models.BooleanField(default=True, verbose_name=b'Show this Title on Scribl')),
                ('date_accepted', models.DateTimeField(null=True, verbose_name=b'Date Terms and Conditions for this Title Accepted by Author')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created', db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name=b'Date Updated', db_index=True)),
                ('awards', models.ManyToManyField(related_name=b'titles', null=True, to='core.Award', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(related_name=b'titlecategories', to='core.Category')),
                ('title', models.ForeignKey(related_name=b'titlecategories', to='core.Title')),
            ],
            options={
                'verbose_name_plural': 'Title Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitleContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('contributor', models.ForeignKey(related_name=b'titlecontributors', to='core.Contributor')),
                ('contributor_type', models.ForeignKey(related_name=b'titlecontributors', to='core.ContributorType')),
                ('title', models.ForeignKey(related_name=b'titlecontributors', to='core.Title')),
            ],
            options={
                'ordering': ['contributor_type__slug', 'date_created'],
                'verbose_name_plural': 'Title Contributors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitleUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('linktext', models.CharField(max_length=255)),
                ('displayorder', models.IntegerField(default=1)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('title', models.ForeignKey(related_name=b'urls', to='core.Title')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='title',
            name='categories',
            field=models.ManyToManyField(to='core.Category', through='core.TitleCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='contributors',
            field=models.ManyToManyField(to='core.Contributor', through='core.TitleContributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='license',
            field=models.ForeignKey(related_name=b'titles', to='core.License', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='series',
            field=models.ForeignKey(related_name=b'titles', blank=True, to='core.Series', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='media',
            name='title',
            field=models.ForeignKey(related_name=b'media', to='core.Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='contributors',
            field=models.ManyToManyField(to='core.Contributor', through='core.EpisodeContributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='title',
            field=models.ForeignKey(related_name=b'episodes', to='core.Title'),
            preserve_default=True,
        ),
    ]
