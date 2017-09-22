#!/usr/bin/env python
# encoding: utf-8
from peewee import *

import config
from playhouse.pool import PooledMySQLDatabase


mysql_db = PooledMySQLDatabase(config.get('database_db_name'), max_connections=8, stale_timeout=300,
                                                            **{'host': config.get('database_host'),
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
    name = CharField()
    student_id = CharField()
    department = CharField(null=True)
    grade = CharField(null=True)
    major = CharField(null=True)
    sex = CharField(null=True)
    class_id = CharField(null=True)
    # cas_id = CharField(null=True)
    student_status = CharField(null=True)
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
            mobile=info['mobile'],
            card_id=info['card_id'],
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
    def saveInfo(cls, student_id, info):
        u = cls.select().where(cls.student_id == student_id).get()
        if u is not None:
            return u
        else:
            cls.addUser(info)
            return cls.select().where(cls.student_id == student_id).get()

    @classmethod
    def getInfo(cls, student_id, password):
        u = cls.select().where(cls.student_id==student_id, cls.password==password)
        for n in u:
            return n
