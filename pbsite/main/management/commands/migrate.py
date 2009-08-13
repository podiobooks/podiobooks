'''
Created on Aug 04, 2009

migrate.py - Django command to migrate an initial import from PB1 to the final schema.  This code is specific
to PostgreSQL and intended for production migration.  

@author: cmdln
'''

import os.path
import datetime

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db import models



class Command(BaseCommand):
    def __init__(self):
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
        cursor.execute(drop_all)

        self.__migrate_category(cursor)
        self.__migrate_partner(cursor)
        self.__migrate_user(cursor)
        self.__migrate_book(cursor)

        transaction.commit_unless_managed()

        elapsed = datetime.datetime.now() - start

        print 'Took %s to complete migration.' % elapsed


    def __migrate_category(self, cursor):
        ops = [AddColumn(models.SlugField(name='slug'),
                         update="lower(regexp_replace(name, ' ', '-'))"),
               AddColumn(models.BooleanField(name='deleted', default='false', null=False)),
               AddColumn(models.DateTimeField(name='date_created', default='now()', null=False)),
               AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
               AlterColumnType(models.CharField(name='name',
                                                max_length=255),
                               using="substr(trim(both ' ' from name), 0, 255)"),
               DropDefault('name'),
               DropColumn('display'),
               DropColumn('parentcatid'),
               DropColumn('itunesxml'),
            ]
        self.__migrate_table(cursor, 'bookcategory', 'main_category', ops)


    def __migrate_partner(self, cursor):
        ops = [AddColumn(models.IntegerField(name='old_id', null=True)),
               AddColumn(models.BooleanField(name='deleted', default='false', null=False)),
               AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
               DropDefault('name'),
               DropDefault('url'),
               AlterColumnType(models.CharField(name='url',
                                                max_length=200),
                               using="substr(trim(both ' ' from url), 0, 200)"),
               DropDefault('logo'),
               AlterColumnType(models.CharField(name='logo',
                                                max_length=100),
                               using="substr(trim(both ' ' from logo), 0, 100)"),
               RenameColumn('datecreated', 'date_created'),
               DropDefault('date_created'),
               AlterColumnType(models.DateTimeField(name='date_created')),
               DropColumn('css'),
               DropColumn('enabled'),
               DropColumn('haslibrary'),
               DropColumn('headerhtml'),
               DropColumn('footerhtml'),
            ]
        self.__migrate_table(cursor, 'partner', 'main_partner', ops)


    def __migrate_user(self, cursor):
        ops = [AddColumn(models.BooleanField(name='is_staff',
                                             default='false',
                                             null=False),
                         update='roleid > 2'),
               AddColumn(models.BooleanField(name='is_superuser',
                                             null=False),
                         update='roleid = 4'),
               AddColumn(models.DateTimeField(name='last_login',
                                              null=False),
                         update="timestamp 'epoch'"),
               RenameColumn('handle', 'username'),
               AlterColumnType(models.CharField(name='username',
                                                 max_length=30),
                               using='trim(both ' ' from username)'),
               DropDefault('username'),
               RenameColumn('firstname', 'first_name'),
               AlterColumnType(models.CharField(name='first_name',
                                                 max_length=30),
                               using='substr(trim(both ' ' from first_name), 0, 30)'),
               DropDefault('first_name'),
               RenameColumn('lastname', 'last_name'),
               AlterColumnType(models.CharField(name='last_name',
                                                 max_length=30),
                               using='substr(trim(both ' ' from last_name), 0, 30)'),
               DropDefault('last_name'),
               AlterColumnType(models.CharField(name='email',
                                                 max_length=75)),
               DropDefault('email'),
               AlterColumnType(models.CharField(name='password',
                                                 max_length=128)),
               DropDefault('password'),
               DropConstraint('user_enabled_check'),
               RenameColumn('enabled', 'is_active'),
               DropDefault('is_active'),
               AlterColumnType(models.BooleanField(name='is_active'),
                               using='is_active = 1'),
               RenameColumn('datecreated', 'date_joined'),
               AlterColumnType(models.DateTimeField(name='date_joined')),
               DropDefault('date_joined'),
               DropColumn('userstatusid'),
               DropColumn('roleid'),
               DropColumn('partnerid')
            ]
        self.__migrate_table(cursor, 'public.user', 'auth_user', ops)


    def __migrate_book(self, cursor):
        ops = [
               # TODO add FK to series in books.sql
               RenameColumn('title', 'name'),
               DropDefault('name'),
               AddColumn(models.SlugField(name='slug',
                                          null=False),
                         update="lower(substr(regexp_replace(name, ' ', '-'), 0, 50))"),
               RenameColumn('coverimage', 'cover'),
               AlterColumnType(models.CharField(name='cover',
                                                max_length=100,
                                                default="substr(trim(both ' ' from cover), 0, 100)")),
               DropDefault('cover'),
               # TODO calculate status from standby/complete?!
               AddColumn(models.IntegerField(name='status', default='0')),
               # TODO need to match up strings to fixture values
               AddColumn(models.IntegerField(name='license_id', null=True)),
               AddForeignKey('license_id', 'main_license'),
               DropConstraint('book_displayonhomepage_check'),
               RenameColumn('displayonhomepage', 'display_on_homepage'),
               DropDefault('display_on_homepage'),
               AlterColumnType(models.BooleanField(name='display_on_homepage'),
                               using='display_on_homepage = 1'),
               AddColumn(models.BooleanField(name='is_hosted_at_pb', null=False, default='true')),
               # TODO need to match up explicit flag to fixture values
               AddColumn(models.IntegerField(name='advisory_id', null=True)),
               AddForeignKey('advisory_id', 'main_advisory'),
               DropConstraint('book_explicit_check'),
               RenameColumn('explicit', 'is_adult'),
               DropDefault('is_adult'),
               AlterColumnType(models.BooleanField(name='is_adult'),
                               using='is_adult = 1'),
               AddColumn(models.IntegerField(name='series_id', null=True)),
               AddForeignKey('series_id', 'main_series'),
               RenameColumn('complete', 'is_complete'),
               DropDefault('is_complete'),
               AlterColumnType(models.BooleanField(name='is_complete'),
                               using="is_complete = '1'"),
               RenameColumn('avgaudioquality', 'avg_audio_quality'),
               SetNotNull('avg_audio_quality', '0.0'),
               Rollback()
              ]
        self.__migrate_table(cursor, 'book', 'main_book', ops)


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
                    operation.table_name = new_name
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
