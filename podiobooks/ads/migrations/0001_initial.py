# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AdSchedule' -- Manual fix to ensure table is built from scratch
        db.delete_table('ads_adschedule')

        # Adding model 'AdSchedule'
        db.create_table('ads_adschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ads', ['AdSchedule'])

        # Adding M2M table for field titles on 'AdSchedule'
        m2m_table_name = db.shorten_name('ads_adschedule_titles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('adschedule', models.ForeignKey(orm['ads.adschedule'], null=False)),
            ('title', models.ForeignKey(orm['core.title'], null=False))
        ))
        db.create_unique(m2m_table_name, ['adschedule_id', 'title_id'])

        # Adding model 'AdSchedulePosition'
        db.create_table('ads_adscheduleposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad_schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ad_schedule_positions', to=orm['ads.AdSchedule'])),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ad_schedule_episodes', to=orm['core.Episode'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ads', ['AdSchedulePosition'])


    def backwards(self, orm):
        # Deleting model 'AdSchedule'
        db.delete_table('ads_adschedule')

        # Removing M2M table for field titles on 'AdSchedule'
        db.delete_table(db.shorten_name('ads_adschedule_titles'))

        # Deleting model 'AdSchedulePosition'
        db.delete_table('ads_adscheduleposition')


    models = {
        'ads.adschedule': {
            'Meta': {'ordering': "['name']", 'object_name': 'AdSchedule'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'titles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ad_schedules'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Title']"})
        },
        'ads.adscheduleposition': {
            'Meta': {'ordering': "['ad_schedule__name']", 'object_name': 'AdSchedulePosition'},
            'ad_schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ad_schedule_positions'", 'to': "orm['ads.AdSchedule']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ad_schedule_episodes'", 'to': "orm['core.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.award': {
            'Meta': {'ordering': "['name']", 'object_name': 'Award'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'core.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'core.contributor': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Contributor'},
            'community_handle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contributor_info'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'core.contributortype': {
            'Meta': {'object_name': 'ContributorType'},
            'byline_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'core.episode': {
            'Meta': {'ordering': "['title__name', 'sequence']", 'object_name': 'Episode'},
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Contributor']", 'through': "orm['core.EpisodeContributor']", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'45:00'", 'max_length': '20'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.episodecontributor': {
            'Meta': {'object_name': 'EpisodeContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['core.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['core.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['core.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.license': {
            'Meta': {'ordering': "['slug']", 'object_name': 'License'},
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.series': {
            'Meta': {'ordering': "['name']", 'object_name': 'Series'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'core.title': {
            'Meta': {'ordering': "['name']", 'object_name': 'Title'},
            'awards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Award']"}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'through': "orm['core.TitleCategory']", 'symmetrical': 'False'}),
            'category_list': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Contributor']", 'through': "orm['core.TitleContributor']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'detractor_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'display_on_homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_adult': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_explicit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_family_friendly': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_for_kids': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'itunes_adam_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'itunes_new_feed_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '10', 'db_index': 'True'}),
            'libsyn_show_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': "orm['core.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'podiobooker_blog_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'promoter_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': "orm['core.Series']"}),
            'series_sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'core.titlecategory': {
            'Meta': {'object_name': 'TitleCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecategories'", 'to': "orm['core.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecategories'", 'to': "orm['core.Title']"})
        },
        'core.titlecontributor': {
            'Meta': {'ordering': "['contributor_type__slug', 'date_created']", 'object_name': 'TitleContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['core.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['core.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['core.Title']"})
        }
    }

    complete_apps = ['ads']