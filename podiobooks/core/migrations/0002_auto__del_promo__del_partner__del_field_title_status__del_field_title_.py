# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Promo'
        db.delete_table('core_promo')

        # Deleting model 'Partner'
        db.delete_table('core_partner')

        # Deleting field 'Title.status'
        db.delete_column('core_title', 'status')

        # Deleting field 'Title.avg_audio_quality'
        db.delete_column('core_title', 'avg_audio_quality')

        # Deleting field 'Title.avg_overall'
        db.delete_column('core_title', 'avg_overall')

        # Deleting field 'Title.partner'
        db.delete_column('core_title', 'partner_id')

        # Deleting field 'Title.is_hosted_at_pb'
        db.delete_column('core_title', 'is_hosted_at_pb')

        # Deleting field 'Title.avg_narration'
        db.delete_column('core_title', 'avg_narration')

        # Deleting field 'Title.avg_writing'
        db.delete_column('core_title', 'avg_writing')

        # Deleting field 'Title.is_complete'
        db.delete_column('core_title', 'is_complete')


    def backwards(self, orm):
        # Adding model 'Promo'
        db.create_table('core_promo', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='promos', to=orm['core.Title'])),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Promo'])

        # Adding model 'Partner'
        db.create_table('core_partner', (
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Partner'])

        # Adding field 'Title.status'
        db.add_column('core_title', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Title.avg_audio_quality'
        db.add_column('core_title', 'avg_audio_quality',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Title.avg_overall'
        db.add_column('core_title', 'avg_overall',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Title.partner'
        db.add_column('core_title', 'partner',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', null=True, to=orm['core.Partner'], blank=True),
                      keep_default=False)

        # Adding field 'Title.is_hosted_at_pb'
        db.add_column('core_title', 'is_hosted_at_pb',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Title.avg_narration'
        db.add_column('core_title', 'avg_narration',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Title.avg_writing'
        db.add_column('core_title', 'avg_writing',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Title.is_complete'
        db.add_column('core_title', 'is_complete',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'displaytext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hexcolor': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
        'core.media': {
            'Meta': {'ordering': "['name']", 'object_name': 'Media'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Print Version'", 'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'core.rating': {
            'Meta': {'object_name': 'Rating'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_rating_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
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
            'advisory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': "orm['core.Advisory']"}),
            'awards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Award']"}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'through': "orm['core.TitleCategory']", 'symmetrical': 'False'}),
            'category_list': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Contributor']", 'through': "orm['core.TitleContributor']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'detractor_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'display_on_homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_adult': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_explicit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'itunes_adam_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'libsyn_show_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': "orm['core.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        },
        'core.titleurl': {
            'Meta': {'object_name': 'TitleUrl'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'displayorder': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linktext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['core.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']