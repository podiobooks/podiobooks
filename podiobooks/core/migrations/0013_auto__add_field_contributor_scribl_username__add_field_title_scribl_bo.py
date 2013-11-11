# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contributor.scribl_username'
        db.add_column(u'core_contributor', 'scribl_username',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Title.scribl_book_id'
        db.add_column(u'core_title', 'scribl_book_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Contributor.scribl_username'
        db.delete_column(u'core_contributor', 'scribl_username')

        # Deleting field 'Title.scribl_book_id'
        db.delete_column(u'core_title', 'scribl_book_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.award': {
            'Meta': {'ordering': "['name']", 'object_name': 'Award'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'core.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'core.contributor': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Contributor'},
            'community_handle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'scribl_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contributor_info'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'core.contributortype': {
            'Meta': {'object_name': 'ContributorType'},
            'byline_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'core.episode': {
            'Meta': {'ordering': "['title__name', 'sequence']", 'object_name': 'Episode'},
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Contributor']", 'through': u"orm['core.EpisodeContributor']", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'45:00'", 'max_length': '20'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_date_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': u"orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'core.episodecontributor': {
            'Meta': {'object_name': 'EpisodeContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': u"orm['core.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': u"orm['core.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': u"orm['core.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.license': {
            'Meta': {'ordering': "['slug']", 'object_name': 'License'},
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'core.media': {
            'Meta': {'ordering': "['name']", 'object_name': 'Media'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Print Version'", 'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media'", 'to': u"orm['core.Title']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'core.rating': {
            'Meta': {'object_name': 'Rating'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_rating_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'core.series': {
            'Meta': {'ordering': "['name']", 'object_name': 'Series'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.title': {
            'Meta': {'ordering': "['name']", 'object_name': 'Title'},
            'awards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Award']"}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Category']", 'through': u"orm['core.TitleCategory']", 'symmetrical': 'False'}),
            'category_list': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Contributor']", 'through': u"orm['core.TitleContributor']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'detractor_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'display_on_homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_adult': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_explicit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_family_friendly': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_for_kids': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'itunes_adam_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'itunes_new_feed_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '10', 'db_index': 'True'}),
            'libsyn_show_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': u"orm['core.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'podiobooker_blog_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'promoter_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'scribl_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scribl_book_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': u"orm['core.Series']"}),
            'series_sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'tips_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.titlecategory': {
            'Meta': {'object_name': 'TitleCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecategories'", 'to': u"orm['core.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecategories'", 'to': u"orm['core.Title']"})
        },
        u'core.titlecontributor': {
            'Meta': {'ordering': "['contributor_type__slug', 'date_created']", 'object_name': 'TitleContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': u"orm['core.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': u"orm['core.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': u"orm['core.Title']"})
        },
        u'core.titleurl': {
            'Meta': {'object_name': 'TitleUrl'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'displayorder': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linktext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': u"orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']