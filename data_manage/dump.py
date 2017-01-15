from peewee import *

database = MySQLDatabase('school_service', **{'host': '127.0.0.1', 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class I(BaseModel):
    birthday = CharField(null=True)
    bound = IntegerField()
    card = CharField(db_column='card_id', null=True)
    cas = CharField(db_column='cas_id', null=True)
    class_ = CharField(db_column='class_id', null=True)
    department = CharField(null=True)
    ecard = CharField(db_column='ecard_id', null=True)
    grade = CharField(null=True)
    major = CharField(null=True)
    mobile = CharField(null=True)
    name = CharField()
    password = CharField(null=True)
    sex = CharField(null=True)
    student = CharField(db_column='student_id')
    student_status = CharField(null=True)

    class Meta:
        db_table = 'i'

class User(BaseModel):
    birthday = CharField(null=True)
    bound = IntegerField()
    card = CharField(db_column='card_id', null=True)
    class_ = CharField(db_column='class_id')
    department = CharField()
    ecard = CharField(db_column='ecard_id', null=True)
    grade = CharField()
    major = CharField()
    mobile = CharField(null=True)
    name = CharField()
    password = CharField(null=True)
    sex = CharField()
    student = CharField(db_column='student_id')
    student_status = CharField()

    class Meta:
        db_table = 'user'



def d():
    for n in User.select():
        person, created = I.get_or_create(
            student = n.student,
            defaults={
                'name' : n.name,
                'student' : n.student,
                'department' : n.department,
                'grade' : n.grade,
                'major' : n.major,
                'sex' : n.sex,
                'class_' : n.class_,
                'student_status' : n.student_status
            }
        )
        if person:
            person.department = n.department
            person.grade = n.grade
            person.major = n.major
            person.sex = n.sex
            person.class_ = n.class_
            person.student_status = n.student_status
            person.save()


d()
