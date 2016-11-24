#!/usr/bin/env python
# encoding: utf-8
from peewee import *
import config

mysql_db = MySQLDatabase(config.get('database_db_name'), **{'host': config.get('database_host'),
                                                            'user': config.get('database_user'),
                                                            'password': config.get('database_password'),
                                                            'port': config.get('database_port')}
                         )

class User(Model):
    username = CharField()
    password = CharField()
    encode_password = CharField()

    class Meta:
        database = mysql_db