# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Advisory'
        db.create_table('main_advisory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('displaytext', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hexcolor', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 210254))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 210287))),
        ))
        db.send_create_signal('main', ['Advisory'])

        # Adding model 'Award'
        db.create_table('main_award', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 211012))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 211042))),
        ))
        db.send_create_signal('main', ['Award'])

        # Adding model 'Category'
        db.create_table('main_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 211947))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 211981))),
        ))
        db.send_create_signal('main', ['Category'])

        # Adding model 'Contributor'
        db.create_table('main_contributor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=1000, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contributor_info', null=True, to=orm['auth.User'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 212676))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 212700))),
        ))
        db.send_create_signal('main', ['Contributor'])

        # Adding model 'ContributorType'
        db.create_table('main_contributortype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('byline_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('main', ['ContributorType'])

        # Adding model 'Episode'
        db.create_table('main_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='episodes', to=orm['main.Title'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('filesize', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('length', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 234247))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 234285))),
        ))
        db.send_create_signal('main', ['Episode'])

        # Adding model 'EpisodeContributor'
        db.create_table('main_episodecontributor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='episodecontributors', to=orm['main.Episode'])),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='episodecontributors', to=orm['main.Contributor'])),
            ('contributor_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='episodecontributors', to=orm['main.ContributorType'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 235365))),
        ))
        db.send_create_signal('main', ['EpisodeContributor'])

        # Adding model 'License'
        db.create_table('main_license', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 266536))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 266574))),
        ))
        db.send_create_signal('main', ['License'])

        # Adding model 'Media'
        db.create_table('main_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media', to=orm['main.Title'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('baseurl', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 267301))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 267332))),
        ))
        db.send_create_signal('main', ['Media'])

        # Adding model 'Partner'
        db.create_table('main_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 267981))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 268011))),
        ))
        db.send_create_signal('main', ['Partner'])

        # Adding model 'Promo'
        db.create_table('main_promo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='promos', to=orm['main.Title'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 268778))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 268808))),
        ))
        db.send_create_signal('main', ['Promo'])

        # Adding model 'Rating'
        db.create_table('main_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_rating_id', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 269341))),
        ))
        db.send_create_signal('main', ['Rating'])

        # Adding model 'Series'
        db.create_table('main_series', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 271855))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 271888))),
        ))
        db.send_create_signal('main', ['Series'])

        # Adding model 'Title'
        db.create_table('main_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', null=True, to=orm['main.Series'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', null=True, to=orm['main.License'])),
            ('display_on_homepage', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_hosted_at_pb', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('advisory', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='titles', null=True, to=orm['main.Advisory'])),
            ('is_adult', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_explicit', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('avg_audio_quality', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('avg_narration', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('avg_writing', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('avg_overall', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('promoter_count', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('detractor_count', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('category_list', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='titles', null=True, to=orm['main.Partner'])),
            ('libsyn_show_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('itunes_adam_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('podiobooker_blog_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 273287), db_index=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 273322), db_index=True)),
        ))
        db.send_create_signal('main', ['Title'])

        # Adding M2M table for field awards on 'Title'
        db.create_table('main_title_awards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.ForeignKey(orm['main.title'], null=False)),
            ('award', models.ForeignKey(orm['main.award'], null=False))
        ))
        db.create_unique('main_title_awards', ['title_id', 'award_id'])

        # Adding model 'TitleCategory'
        db.create_table('main_titlecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titlecategories', to=orm['main.Title'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titlecategories', to=orm['main.Category'])),
        ))
        db.send_create_signal('main', ['TitleCategory'])

        # Adding model 'TitleContributor'
        db.create_table('main_titlecontributor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titlecontributors', to=orm['main.Title'])),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titlecontributors', to=orm['main.Contributor'])),
            ('contributor_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titlecontributors', to=orm['main.ContributorType'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 293954))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 293989))),
        ))
        db.send_create_signal('main', ['TitleContributor'])

        # Adding model 'TitleUrl'
        db.create_table('main_titleurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(related_name='urls', to=orm['main.Title'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('linktext', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('displayorder', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 294747))),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 7, 9, 13, 33, 294777))),
        ))
        db.send_create_signal('main', ['TitleUrl'])


    def backwards(self, orm):
        
        # Deleting model 'Advisory'
        db.delete_table('main_advisory')

        # Deleting model 'Award'
        db.delete_table('main_award')

        # Deleting model 'Category'
        db.delete_table('main_category')

        # Deleting model 'Contributor'
        db.delete_table('main_contributor')

        # Deleting model 'ContributorType'
        db.delete_table('main_contributortype')

        # Deleting model 'Episode'
        db.delete_table('main_episode')

        # Deleting model 'EpisodeContributor'
        db.delete_table('main_episodecontributor')

        # Deleting model 'License'
        db.delete_table('main_license')

        # Deleting model 'Media'
        db.delete_table('main_media')

        # Deleting model 'Partner'
        db.delete_table('main_partner')

        # Deleting model 'Promo'
        db.delete_table('main_promo')

        # Deleting model 'Rating'
        db.delete_table('main_rating')

        # Deleting model 'Series'
        db.delete_table('main_series')

        # Deleting model 'Title'
        db.delete_table('main_title')

        # Removing M2M table for field awards on 'Title'
        db.delete_table('main_title_awards')

        # Deleting model 'TitleCategory'
        db.delete_table('main_titlecategory')

        # Deleting model 'TitleContributor'
        db.delete_table('main_titlecontributor')

        # Deleting model 'TitleUrl'
        db.delete_table('main_titleurl')


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
        'main.advisory': {
            'Meta': {'ordering': "['name']", 'object_name': 'Advisory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 210254)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 210287)'}),
            'displaytext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hexcolor': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'main.award': {
            'Meta': {'ordering': "['name']", 'object_name': 'Award'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 211012)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 211042)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'main.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 211947)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 211981)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'main.contributor': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Contributor'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 212676)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 212700)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '1000', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contributor_info'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'main.contributortype': {
            'Meta': {'object_name': 'ContributorType'},
            'byline_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'main.episode': {
            'Meta': {'ordering': "['title__name', 'sequence']", 'object_name': 'Episode'},
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Contributor']", 'through': "orm['main.EpisodeContributor']", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 234247)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 234285)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['main.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'main.episodecontributor': {
            'Meta': {'object_name': 'EpisodeContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['main.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['main.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 235365)'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodecontributors'", 'to': "orm['main.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.license': {
            'Meta': {'ordering': "['slug']", 'object_name': 'License'},
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 266536)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 266574)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'main.media': {
            'Meta': {'ordering': "['name']", 'object_name': 'Media'},
            'baseurl': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 267301)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 267332)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media'", 'to': "orm['main.Title']"})
        },
        'main.partner': {
            'Meta': {'ordering': "['name']", 'object_name': 'Partner'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 267981)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 268011)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'main.promo': {
            'Meta': {'ordering': "['name']", 'object_name': 'Promo'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 268778)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 268808)'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'promos'", 'to': "orm['main.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'main.rating': {
            'Meta': {'object_name': 'Rating'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 269341)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_rating_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        'main.series': {
            'Meta': {'ordering': "['name']", 'object_name': 'Series'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 271855)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 271888)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'main.title': {
            'Meta': {'ordering': "['name']", 'object_name': 'Title'},
            'advisory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': "orm['main.Advisory']"}),
            'avg_audio_quality': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_narration': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_overall': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'avg_writing': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'awards': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['main.Award']"}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Category']", 'through': "orm['main.TitleCategory']", 'symmetrical': 'False'}),
            'category_list': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Contributor']", 'through': "orm['main.TitleContributor']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 273287)', 'db_index': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 273322)', 'db_index': 'True'}),
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
            'license': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': "orm['main.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'titles'", 'null': 'True', 'to': "orm['main.Partner']"}),
            'podiobooker_blog_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'promoter_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'null': 'True', 'to': "orm['main.Series']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'main.titlecategory': {
            'Meta': {'object_name': 'TitleCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecategories'", 'to': "orm['main.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecategories'", 'to': "orm['main.Title']"})
        },
        'main.titlecontributor': {
            'Meta': {'ordering': "['contributor_type__slug', 'date_created']", 'object_name': 'TitleContributor'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['main.Contributor']"}),
            'contributor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['main.ContributorType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 293954)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 293989)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlecontributors'", 'to': "orm['main.Title']"})
        },
        'main.titleurl': {
            'Meta': {'object_name': 'TitleUrl'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 294747)'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 7, 9, 13, 33, 294777)'}),
            'displayorder': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linktext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['main.Title']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['main']
