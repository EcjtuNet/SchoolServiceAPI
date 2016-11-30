#!/usr/bin/env python
# encoding: utf-8
from peewee import *

import config

mysql_db = MySQLDatabase(config.get('database_db_name'), **{'host': config.get('database_host'),
                                                            'user': config.get('database_user'),
                                                            'password': config.get('database_password'),
                                                            'port': config.get('database_port'),
                                                            'charset': config.get('database_charset')}
                         )

class BaseModel(Model):
    class Meta:
        database = mysql_db


class User(BaseModel):
    id = PrimaryKeyField()
    department = CharField()
    grade = CharField()
    major = CharField()
    name = CharField()
    sex = CharField()
    class_id = CharField()
    student_id = CharField()
    student_status = CharField()
    card_id = CharField(null=True)
    ecard_id = CharField(null=True)
    birthday = CharField(null=True)
    mobile = CharField(null=True)
    password = CharField(null=True)
    bound = BooleanField(default=False)


    class Meta:
        db_table = 'user'

    @classmethod
    def addUser(cls, info):
        cls.create(
            department=info['department'],
            grade=info['grade'],
            major=info['major'],
            name=info['name'],
            sex=info['sex'],
            class_id=info['class_id'],
            student_id=info['student_id'],
            student_status=info['student_status']
        )


    @classmethod
    def getName(cls, student_id):
        na = cls.select().where(cls.student_id==student_id)
        for n in na:
            return n.name


    @classmethod
    def savePassword(cls, student_id, password):
        u = cls.select().where(cls.student_id==student_id)
        for n in u:
            n.password = password
            n.bound = True
            n.save()
            return n


    @classmethod
    def saveInfo(cls, student_id, card_id, birthday, mobile):
        u = cls.select().where(cls.student_id==student_id)
        for n in u:
            n.card_id = card_id
            n.birthday = birthday
            n.mobile = mobile
            n.save()
            return n

    @classmethod
    def getInfo(cls, student_id, password):
        u = cls.select().where(cls.student_id==student_id, cls.password==password)
        for n in u:
            return n
