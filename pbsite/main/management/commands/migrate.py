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
                                DropColumn('display'),
                                DropColumn('parentcatid'),
                                DropColumn('itunesxml'),
                                AddColumn(models.SlugField(name='slug',
                                                           default="lower(regexp_replace(name, ' ', '-'))")),
                                AddColumn(models.BooleanField(name='deleted', default='false')),
                                AddColumn(models.DateTimeField(name='date_created', default='now()')),
                                AddColumn(models.DateTimeField(name='date_updated', default='now()')),
                                'category.sql'
                             ])

        self.__migrate_table(cursor, 'public.user', 'auth_user',
                             [
                                AddColumn(models.BooleanField(name='is_staff',
                                                              default='roleid > 2')),
                                AddColumn(models.BooleanField(name='is_superuser',
                                                              default='roleid = 4')),
                                AddColumn(models.DateTimeField(name='last_login',
                                                              default="timestamp 'epoch'")),
                                DropColumn('userstatusid'),
                                DropColumn('roleid'),
                                DropColumn('partnerid'),
                                'user.sql'
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
        sql = 'alter table %s drop column %s' % (self.table_name, self.name)
        cursor.execute(sql)


class AddColumn:
    def __init__(self, field):
        self.field = field
        self.table_name = None


    def migrate(self, cursor):
        sql = 'alter table %s add column %s %s;' % (self.table_name, self.field.name, self.field.db_type())
        cursor.execute(sql)
        sql = 'update %s set %s = %s;' % (self.table_name, self.field.name, self.field.default)
        cursor.execute(sql)
        sql = 'alter table %s alter column %s set not null' % (self.table_name, self.field.name)
        cursor.execute(sql)
