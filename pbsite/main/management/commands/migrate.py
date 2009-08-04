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

        self.__migrate_table(cursor, 'bookcategory', 'main_category',
                             [
                                AddColumn(models.SlugField(name='slug',
                                                           default="lower(regexp_replace(name, ' ', '-'))")),
                                AddColumn(models.BooleanField(name='deleted', default='false', null=False)),
                                AddColumn(models.DateTimeField(name='date_created', default='now()', null=False)),
                                AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
                                DropColumn('display'),
                                DropColumn('parentcatid'),
                                DropColumn('itunesxml'),
                                'category.sql'
                             ])
        
        self.__migrate_table(cursor, 'partner', 'main_partner',
                             [
                                AddColumn(models.IntegerField(name='old_id', null=True)),
                                AddColumn(models.BooleanField(name='deleted', default='false', null=False)),
                                AddColumn(models.DateTimeField(name='date_updated', default='now()', null=False)),
                                DropColumn('css'),
                                DropColumn('enabled'),
                                DropColumn('haslibrary'),
                                DropColumn('headerhtml'),
                                DropColumn('footerhtml'),
                                'partner.sql'
                             ])

        self.__migrate_table(cursor, 'public.user', 'auth_user',
                             [
                                AddColumn(models.BooleanField(name='is_staff',
                                                              default='roleid > 2', null=False)),
                                AddColumn(models.BooleanField(name='is_superuser',
                                                              default='roleid = 4', null=False)),
                                AddColumn(models.DateTimeField(name='last_login',
                                                              default="timestamp 'epoch'", null=False)),
                                DropColumn('userstatusid'),
                                DropColumn('roleid'),
                                DropColumn('partnerid'),
                                'user.sql'
                             ])
        
        self.__migrate_table(cursor, 'book', 'main_book',
                             [
                                RenameColumn('title', 'name'),
                                DropColumnConstraint('name'),
                                AddColumn(models.ForeignKey('Series', null=True)),
                                AddColumn(models.SlugField(name='slug',
                                                           default="lower(substr(regexp_replace(name, ' ', '-'), 0, 50))",
                                                           null=False)),
                                RenameColumn('coverimage', 'cover'),
                                AlterColumnType(models.CharField(max_length=100,
                                                                 default="substr(trim(both ' ' from cover), 0, 100)")),
                                DropColumnConstraint('cover'),
                                # TODO calculate status from standby/complete?!
                                AddColumn(models.IntegerField(name='status', default='0')),
                                # TODO need to match up strings to fixture values
                                AddColumn(models.ForeignKey('License', null=True)),
                                RenameColumn('displayonhomepage', 'display_on_homepage'),
                                AlterColumnType(models.BooleanField(name='display_on_homepage',
                                                                    default='display_on_homepage = 1')),
                                DropColumnConstraint('display_on_homepage'),
                                AddColumn(models.BooleanField(name='is_hosted_at_pb', default='true')),
                                # TODO need to match up explicit flag to fixture values
                                AddColumn(models.ForeignKey('Advisory', null=True)),
                             ])

        transaction.commit_unless_managed()

        elapsed = datetime.datetime.now() - start

        print 'Took %s to complete migration.' % elapsed


    def __migrate_table(self, cursor, name, new_name, operations):
        print 'Migrating %s to %s' % (name, new_name)

        cursor.execute('alter table %s rename to %s' % (name, new_name))
        cursor.execute('alter sequence %s_id_seq rename to %s_id_seq' % (name, new_name))
        
        for operation in operations:
            if operation.__class__ == str:
                op_sql = self.__load_sql(operation)
                cursor.execute(op_sql)
            else:
                operation.table_name = new_name
                operation.migrate(cursor)

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


class DropColumn:
    def __init__(self, name):
        self.name = name
        self.table_name = None


    def migrate(self, cursor):
        sql = 'alter table %s drop column %s;' % (self.table_name, self.name)
        cursor.execute(sql)


class AddColumn:
    def __init__(self, field, null=False):
        self.field = field
        self.table_name = None


    def migrate(self, cursor):
        sql = 'alter table %s add column %s %s;' % (self.table_name, self.field.name, self.field.db_type())
        cursor.execute(sql)
        if not self.field.null:
            sql = 'update %s set %s = %s;' % (self.table_name, self.field.name, self.field.default)
            cursor.execute(sql)
            sql = 'alter table %s alter column %s set not null;' % (self.table_name, self.field.name)
            cursor.execute(sql)


class RenameColumn:
    def __init__(self, old_name, new_name):
        self.old_name
        self.new_name = new_name
        self.table_name = None


    def migrate(self, cursor):
        sql = 'alter table %s rename column %s to %s;' % (self.table_name, self.old_name, self.new_name)
        cursor.execute(sql)


class AlterColumnType:
    def __init__(self, field):
        self.field = field
        self.table_name = None


    def migrate(self, cursor):
        if (self.field.default):
            sql = 'alter table %s alter column %s type %s %s;' % (self.table_name, self.field.name, self.field.db_type, self.field.default)
        else:
            sql = 'alter table %s alter column %s type %s;' % (self.table_name, self.field.name, self.field.db_type)
        cursor.execute(sql)


class DropColumnConstraint:
    def __init__(self, name):
        self.name = name
        self.table_name = None


    def migrate(self, cursor):
        sql = 'alter table %s alter column %s drop default;' % (self.table_name, self.name)
        cursor.execute(sql) 
