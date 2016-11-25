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
    name = CharField()
    sex = CharField()
    class_id = CharField()
    student_id = CharField()
    student_status = CharField()
    bound = BooleanField(default=False)
    password = CharField(null=True)
    encode_password = CharField(null=True)

    class Meta:
        db_table = 'use'

    def addUser(self, info):
        self.create(
            department=info.department,
            grade=info.grade,
            name=info.name,
            sex=info.sex,
            class_id=info.class_id,
            student_id=info.student_id,
            student_status=info.student_status
        )