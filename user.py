#!/usr/bin/env python
# encoding: utf-8
from peewee import *

mysql_db = MySQLDatabase('school_service', **{'host': 'localhost', 'user': 'root', 'port': 3306})

class User(Model):
    username = CharField()
    password = CharField()
    encode_password = CharField()

    class Meta:
        database = mysql_db