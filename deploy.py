#!/usr/bin/env python
# encoding: utf-8
from user import *
import analyse
import config

# 1
mysql_db.connect()

if ( u'user' not in mysql_db.get_tables() ):
    mysql_db.create_table(User)

# 2
if( config.get('spider')):
    analyse.getStudentList(config.get('student_id'), config.get('cas_password'))

mysql_db.close()
