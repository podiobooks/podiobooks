'''
Created on Aug 04, 2009

migrate.py - Django command to migrate an initial import from PB1 to the final schema.

@author: cmdln
'''

import os.path
import datetime

from django.core.management.base import BaseCommand
from django.db import connection, transaction

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

        # TODO work!

        transaction.commit_unless_managed()
        
        print 'Took %s to complete calculations.' % elapsed

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