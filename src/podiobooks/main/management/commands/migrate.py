'''
Created on Aug 04, 2009

migrate.py - Django command to migrate an initial import from PB1 to the final schema.  This code is specific
to PostgreSQL and intended for production migration.  

@author: cmdln
'''

import os.path
import datetime
import urllib
import urllib2

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db import models

from podiobooks.main.models import License


class Command(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self)
        sql_dir = os.path.abspath(__file__).split("/")
        while sql_dir and sql_dir[-1] != 'commands':
            sql_dir.pop()

        sql_dir.append("sql")
        sql_dir = os.path.join("/", *sql_dir)
        self.sql_dir = sql_dir

    def handle(self, *args, **options):
        start = datetime.datetime.now()

        cursor = connection.cursor()

        drop_all = self.__load_sql('drop_all.sql')
        try:
            cursor.execute(drop_all)
        except:
            pass

        self.__migrate_category(cursor)
        self.__migrate_partner(cursor)
        self.__migrate_user(cursor)
        self.__add_licenses()
        self.__migrate_book(cursor)

        transaction.commit_unless_managed()

        elapsed = datetime.datetime.now() - start

        print 'Took %s to complete migration.' % elapsed


    def __add_licenses(self):
        code_url_template = 'http://creativecommons.org/licenses/%s/3.0/rdf'
        licenses = { 'by' : 'Attribution 3.0 Unported',
                     'by-nd' : 'Attribution-No Derivative Works 3.0 Unported',
                     'by-nc-nd' : 'Attribution-Noncommercial-No Derivative Works 3.0 Unported',
                     'by-nc' : 'Attribution-Noncommercial 3.0 Unported',
                     'by-nc-sa' : 'Attribution-Noncommercial-Share Alike 3.0 Unported',
                     'by-sa' : 'Attribution-Share Alike 3.0 Unported' }
        for (slug, text) in licenses.iteritems():
            license = License()
            license.slug = slug
            
            license.text = text
            
            license.url = 'http://creativecommons.org/licenses/%s/3.0/' % slug
            license.image_url = 'http://i.creativecommons.org/l/%s/3.0/88x31.png' % slug
            
            url = code_url_template % slug
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            license.code = opener.open(urllib2.Request(url)).read()
            license.save()
            

    def __migrate_category(self, cursor):
        ops = [DropConstraint('bookcategory_display_check'),
               AlterVarCharColumn('name', 255),
               AddColumn(models.SlugField(name='slug'),
                         update="lower(regexp_replace(name, ' ', '-'))"),
               AddColumn(models.BooleanField(name='deleted', default='false', null=False)),
               AddColumn(models.DateTimeField(name='date_created', default='now()', null=False)),
               AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
               DropColumns(['display', 'parentcatid', 'itunesxml']),
            ]
        self.__migrate_table(cursor, 'bookcategory', 'main_category', ops)


    def __migrate_partner(self, cursor):
        ops = [RenameColumn('datecreated', 'date_created'),
               DropDefault('name'),
               DropDefault('date_created'),
               AlterVarCharColumn('url', 200),
               AlterVarCharColumn('logo', 100),
               AlterColumnType(models.DateTimeField(name='date_created')),
               AddColumn(models.IntegerField(name='old_id', null=True)),
               AddColumn(models.BooleanField(name='deleted', default='false', null=False)),
               AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
               DropColumns(['css', 'enabled', 'haslibrary', 'headerhtml', 'footerhtml']),
            ]
        self.__migrate_table(cursor, 'partner', 'main_partner', ops)


    def __migrate_user(self, cursor):
        ops = [RenameColumn('handle', 'username'),
               RenameColumn('firstname', 'first_name'),
               RenameColumn('lastname', 'last_name'),
               RenameColumn('enabled', 'is_active'),
               RenameColumn('datecreated', 'date_joined'),
               DropConstraint('user_enabled_check'),
               DropConstraint('user_roleid_check'),
               DropConstraint('user_userstatusid_check'),
               AlterVarCharColumn('username', 30),
               AlterVarCharColumn('first_name', 30),
               AlterVarCharColumn('last_name', 30),
               AlterVarCharColumn('email', 75),
               AlterVarCharColumn('password', 128),
               DropDefault('is_active'),
               AlterColumnType(models.BooleanField(name='is_active'),
                               using='is_active = 1'),
               AlterColumnType(models.DateTimeField(name='date_joined')),
               DropDefault('date_joined'),
               AddColumn(models.BooleanField(name='is_staff',
                                             default='false',
                                             null=False),
                         update='roleid > 2'),
               AddColumn(models.BooleanField(name='is_superuser',
                                             null=False),
                         update='roleid = 4'),
               AddColumn(models.DateTimeField(name='last_login',
                                              null=False),
                         update="timestamp 'epoch'"),
               DropColumns(['userstatusid', 'roleid', 'partnerid'])
            ]
        self.__migrate_table(cursor, 'public.user', 'auth_user', ops)


    def __migrate_book(self, cursor):
        ops = [RenameColumn('title', 'name'),
               RenameColumn('coverimage', 'cover'),
               RenameColumn('displayonhomepage', 'display_on_homepage'),
               RenameColumn('explicit', 'is_adult'),
               RenameColumn('complete', 'is_complete'),
               RenameColumn('avgaudioquality', 'avg_audio_quality'),
               RenameColumn('avgnarration', 'avg_narration'),
               RenameColumn('avgwriting', 'avg_writing'),
               RenameColumn('avgoverall', 'avg_overall'),
               RenameColumn('enabled', 'deleted'),
               RenameColumn('datecreated', 'date_created'),
               DropConstraint('book_categoryid_check'),
               DropConstraint('book_displayonhomepage_check'),
               DropConstraint('book_explicit_check'),
               DropConstraint('book_enabled_check'),
               DropConstraint('book_standby_check'),
               DropConstraint('book_userid_check'),
               DropDefault('name'),
               AlterVarCharColumn('cover', 100),
               DropDefault('display_on_homepage'),
               AlterColumnType(models.BooleanField(name='display_on_homepage'),
                               using='display_on_homepage = 1'),
               DropDefault('is_adult'),
               AlterColumnType(models.BooleanField(name='is_adult'),
                               using='is_adult = 1'),
               DropDefault('is_complete'),
               AlterColumnType(models.BooleanField(name='is_complete'),
                               using="is_complete = '1'"),
               SetNotNull('avg_audio_quality', '0.0'),
               SetNotNull('avg_narration', '0.0'),
               SetNotNull('avg_writing', '0.0'),
               SetNotNull('avg_overall', '0.0'),
               DropDefault('deleted'),
               AlterColumnType(models.BooleanField(name='deleted',
                                                   null=False),
                               using="deleted = 0"),
               AlterColumnType(models.DateTimeField(name='date_created')),
               DropDefault('date_created'),
               AddColumn(models.SlugField(name='slug',
                                          null=False),
                         update="lower(substr(regexp_replace(name, ' ', '-'), 0, 50))"),
               AddColumn(models.IntegerField(name='status', default='1')),
               AddColumn(models.IntegerField(name='license_id', null=True)),
               'update_title_license.sql',
               AddColumn(models.BooleanField(name='is_hosted_at_pb', null=False, default='true')),
               # TODO need to match up explicit flag to fixture values
               AddColumn(models.IntegerField(name='advisory_id', null=True)),
               AddColumn(models.IntegerField(name='series_id', null=True)),
               AddColumn(models.IntegerField(name='old_id', null=True)),
               AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
               AddForeignKey('advisory_id', 'main_advisory'),
               AddForeignKey('license_id', 'main_license'),
               AddForeignKey('series_id', 'main_series'),
               'update_title_license.sql',
               'insert_contributortype.sql',
               'insert_contributor.sql',
               DropColumn('author'),
               DropColumn('userid'),
               # TODO handle partnerid
               DropColumns(['avgrating', 'webpage', 'feedurl', 'subtitle', 'standby',
                            'discussurl', 'notes', 'bookisbn', 'audioisbn', 'ituneslink', 'ebooklink',
                            'lululink', 'dynamicads', 'itunescategory', 'fulllocation', 'fulllength',
                            'fullprice', 'license']),
              ]
        self.__migrate_table(cursor, 'book', 'main_title', ops)


    def __migrate_table(self, cursor, name, new_name, operations):
        print 'Migrating %s to %s' % (name, new_name)

        cursor.execute('alter table %s rename to %s' % (name, new_name))
        cursor.execute('alter sequence %s_id_seq rename to %s_id_seq' % (name, new_name))

        statements = list()
        for operation in operations:
            try:
                if operation.__class__ == str:
                    statements.append(self.__load_sql(operation))
                else:
                    operation.set_table_name(new_name)
                    statements.append(operation.migrate())
            except Exception, e:
                print 'Last operation loaded:\n%s' % operation
                raise e

        for sql in statements:
            try:
                cursor.execute(sql)
            except Exception, e:
                print 'Last SQL statement:\n%s' % sql
                raise e


    def __load_sql(self, file_name):
        sql_file = open(os.path.join(self.sql_dir, file_name))
        sql = ''
        try:
            for line in sql_file:
                sql += line
        finally:
            sql_file.close()

        if not sql:
            raise Exception('Could not load sql file, %s, from directory, %s.' % (file_name, self.sql_dir))
        return sql


class Operation:
    def __init__(self):
        self.table_name = None


    def set_table_name(self, table_name):
        self.table_name = table_name


    def params(self):
        return None


class DropColumn(Operation):
    def __init__(self, name):
        Operation.__init__(self)
        self.name = name


    def __str__(self):
        return 'drop column %s' % self.name


    def migrate(self):
        return 'alter table %s drop column %s;' % (self.table_name, self.name)


class DropColumns(Operation):
    def __init__(self, names):
        Operation.__init__(self)
        self.nested = list()
        for name in names:
            self.nested.append(DropColumn(name))


    def __str__(self):
        return self.nested.__str__()


    def set_table_name(self, table_name):
        Operation.set_table_name(self, table_name)
        [op.set_table_name(table_name) for op in self.nested]


    def migrate(self):
        sql = ''
        for op in self.nested:
            if len(sql) > 1:
                sql += '\n'
            sql += op.migrate()
        return sql


class AddColumn(Operation):
    def __init__(self, field, update=None):
        Operation.__init__(self)
        self.field = field
        self.update = update


    def __str__(self):
        return 'add column %s' % self.field


    def migrate(self):
        if not self.field.null:
            if self.update:
                sql = 'alter table %s add column %s %s null;' % (self.table_name, self.field.name, self.field.db_type())
                sql += '\nupdate %s set %s = %s;' % (self.table_name, self.field.name, self.update)
                sql += '\nalter table %s alter column %s set not null;' % (self.table_name, self.field.name)
            else:
                sql = 'alter table %s add column %s %s not null default %s;' % (self.table_name,
                                                                                self.field.name,
                                                                                self.field.db_type(),
                                                                                self.field.default)
        else:
            sql = 'alter table %s add column %s %s null;' % (self.table_name, self.field.name, self.field.db_type())
        return sql

class RenameColumn(Operation):
    def __init__(self, old_name, new_name):
        Operation.__init__(self)
        self.old_name = old_name
        self.new_name = new_name


    def __str__(self):
        return 'rename column %s to %s' % (self.old_name, self.new_name)


    def migrate(self):
        return 'alter table %s rename column %s to %s;' % (self.table_name, self.old_name, self.new_name)


class DropConstraint(Operation):
    def __init__(self, constraint):
        Operation.__init__(self)
        self.constraint = constraint


    def __str__(self):
        return 'drop constraint %s' % self.constraint


    def migrate(self):
        return 'alter table %s drop constraint %s' % (self.table_name, self.constraint)


class AlterColumnType(Operation):
    def __init__(self, field, using=None):
        Operation.__init__(self)
        self.field = field
        self.using = using


    def __str__(self):
        return 'alter column type %s' % self.field


    def migrate(self):
        if self.using:
            return 'alter table %s alter column %s type %s using %s;' % (self.table_name, self.field.name, self.field.db_type(), self.using)
        else:
            return 'alter table %s alter column %s type %s;' % (self.table_name, self.field.name, self.field.db_type())


class AlterVarCharColumn(Operation):
    def __init__(self, name, max_length):
        Operation.__init__(self)
        self.alter = AlterColumnType(models.CharField(name=name,
                                                      max_length=max_length),
                                     using="substr(trim(both ' ' from %s), 0, %s)" % (name, max_length))
        self.drop_default = DropDefault(name)


    def set_table_name(self, table_name):
        Operation.set_table_name(self, table_name)
        self.alter.set_table_name(table_name)
        self.drop_default.set_table_name(table_name)


    def __str__(self):
        return '%s\n%s' % (self.alter.__str__(), self.drop_default.__str__())


    def migrate(self):
        sql = self.alter.migrate()
        sql += '\n'
        sql += self.drop_default.migrate()
        return sql


class DropDefault(Operation):
    def __init__(self, name):
        Operation.__init__(self)
        self.name = name


    def __str__(self):
        return 'alter column %s drop default' % self.name


    def migrate(self):
        return 'alter table %s alter column %s drop default;' % (self.table_name, self.name)


class SetNotNull(Operation):
    def __init__(self, name, update):
        Operation.__init__(self)
        self.name = name
        self.update = update


    def __str__(self):
        return 'alter column %s set not null' % self.name


    def migrate(self):
        sql = 'update %s set %s = %s;' % (self.table_name, self.name, self.update)
        sql += '\nalter table %s alter column %s set not null;' % (self.table_name, self.name)
        return sql


class DropNotNull(Operation):
    def __init__(self, name):
        Operation.__init__(self)
        self.name = name


    def __str__(self):
        return 'alter column %s drop not null' % self.name


    def migrate(self):
        return 'alter table %s alter column %s drop not null;' % (self.table_name, self.name)


class AddForeignKey(Operation):
    def __init__(self, column, table):
        Operation.__init__(self)
        self.column = column
        self.foreign_table = table


    def __str__(self):
        return 'add constraint %s references %s' % (self.column, self.foreign_table)


    def migrate(self):
        template = 'alter table %(table)s add foreign key (%(column)s) '
        template += 'references %(foreign)s (id) '
        template += 'deferrable initially deferred;'
        return template % {'table': self.table_name,
                           'column': self.column,
                           'foreign': self.foreign_table }


class Rollback(Operation):
    def __init__(self):
        Operation.__init__(self)


    def migrate(self):
        return 'rollback;'
