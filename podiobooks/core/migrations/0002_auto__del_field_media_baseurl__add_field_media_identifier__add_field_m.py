# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Media.baseurl'
        db.delete_column('core_media', 'baseurl')

        # Adding field 'Media.identifier'
        db.add_column('core_media', 'identifier',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Media.url'
        db.add_column('core_media', 'url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Media.baseurl'
        db.add_column('core_media', 'baseurl',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=255),
                      keep_default=False)

        # Deleting field 'Media.identifier'
        db.delete_column('core_media', 'identifier')

        # Deleting field 'Media.url'
        db.delete_column('core_media', 'url')


    models = {
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
        'core.advisory': {
            'Meta': {'ordering': "['name']", 'object_name': 'Advisory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'displaytext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hexcolor': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'core.award': {
            'Meta': {'ordering': "['name']", 'object_name': 'Award'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'core.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'core.contributor': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Contributor'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contributor_info'", 'null': 'True', 'to': "orm['auth.User']"})
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.episodecontributor': {
            'Meta': {'object_name': 'EpisodeContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['core.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['core.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['core.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.license': {
            'Meta': {'ordering': "['slug']", 'object_name': 'License'},
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.media': {
            'Meta': {'ordering': "['name']", 'object_name': 'Media'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Book Version'", 'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'core.partner': {
            'Meta': {'ordering': "['name']", 'object_name': 'Partner'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.promo': {
            'Meta': {'ordering': "['name']", 'object_name': 'Promo'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'promos'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.rating': {
            'Meta': {'object_name': 'Rating'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_rating_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        'core.series': {
            'Meta': {'ordering': "['name']", 'object_name': 'Series'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'core.title': {
            'Meta': {'ordering': "['name']", 'object_name': 'Title'},
            'advisory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': "orm['core.Advisory']"}),
            'avg_audio_quality': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_narration': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_overall': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_writing': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'awards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Award']"}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'through': "orm['core.TitleCategory']", 'symmetrical': 'False'}),
            'category_list': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Contributor']", 'through': "orm['core.TitleContributor']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)', 'db_index': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)', 'db_index': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'detractor_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'display_on_homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_adult': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_explicit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_hosted_at_pb': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'itunes_adam_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'libsyn_show_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': "orm['core.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': "orm['core.Partner']"}),
            'podiobooker_blog_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'promoter_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': "orm['core.Series']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['core.Title']"})
        },
        'core.titleurl': {
            'Meta': {'object_name': 'TitleUrl'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 8, 0, 0)'}),
            'displayorder': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linktext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']