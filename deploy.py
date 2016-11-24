#!/usr/bin/env python
# encoding: utf-8
from user import *

mysql_db.connect()
mysql_db.create_table(User)