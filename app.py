#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request
import time
import json

import analyse
from user import User, mysql_db

app = Flask(__name__)

@app.before_request
def _db_connect():
    mysql_db.connect()

@app.teardown_request
def _db_close(exc):
    if not mysql_db.is_closed():
        mysql_db.close()

# confirm, get开头接口取自数据库
# query开头接口实时获取

@app.route('/api/v1/confirmName', methods=['POST'])
def confirmName():
    student_id = request.form.get('student_id')
    name = User.getName(student_id)
    data = {
        "status":"",
        "data":{
            "name":""
        }
    }
    if (not name):
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['name'] = name[:-1]+"*"
    return json.dumps(data)


@app.route('/api/v1/getName', methods=['POST'])
def getName():
    student_id = request.form.get('student_id')
    name = User.getName(student_id)
    data = {
        "status":"",
        "data":{
            "name":""
        }
    }
    if (not name):
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['name'] = name
    return json.dumps(data)


@app.route('/api/v1/savePassword', methods=['POST'])
def savePassword():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    result = analyse.testPassword(student_id, password)
    data = {
        "status":"",
        "data":{
            "result":""
        }
    }
    if (result == 'error'):
        data['status'] = False
        data['data']['result'] = 'password error'
        return json.dumps(data)
    u = User.savePassword(student_id, password)
    data['status'] = True
    data['data']['result'] = 'password changed'
    return json.dumps(data)


@app.route('/api/v1/saveInfo', methods=['POST'])
def saveInfo():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    user = analyse.saveStudentInfo(student_id, password)
    data = {
        "status":"",
        "data":{
            "user":""
        }
    }
    if (user == 'error'):
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['user'] = user.__dict__['_data']
    return json.dumps(data)


@app.route('/api/v1/getInfo', methods=['POST'])
def getInfo():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    u = User.getInfo(student_id, password)
    data = {
        'status':"",
        'data':{
            "info":""
        }
    }
    if (not u):
        data['status'] = False
        return json.dumps(data)
    info = {
        "department" : u.department,
        "grade" : u.grade,
        "major" : u.major,
        "name" : u.name,
        "sex" : u.sex,
        "class_id" : u.class_id,
        "student_id" : u.student_id,
        "student_status" : u.student_status,
        "card_id" : u.card_id,
        "ecard_id" : u.ecard_id,
        "birthday" : u.birthday,
        "mobile" : u.mobile,
        "bound" : u.bound
    }
    data['status'] = True
    data['data']['info'] = info
    return json.dumps(data)


@app.route('/api/v1/queryScore', methods=['POST'])
def queryScore():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y',time.localtime(time.time())) )-1)
    term = request.form.get('term') if request.form.get('term') else '1'
    if (int(student_id[:4]) >= 2015):
        scoreList = analyse.getScoreFor15(student_id, password, year, term)
    else:
        scoreList = analyse.getScoreFor14(student_id, year, term)
    data = {
        "status":"",
        "data":{
            "score_list":""
        }
    }
    if (scoreList == 'error'):
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['score_list'] = scoreList
    return json.dumps(data)


@app.route('/api/v1/queryDepartment', methods=['GET'])
def queryDepartment():
    dep_list = analyse.getDepartmentListFor14()
    data = {
        "status":"",
        "data":{
            "department_list":""
        }
    }
    data['status'] = True
    data['data']['department_list'] = dep_list
    return json.dumps(data)


@app.route('/api/v1/queryMajor', methods=['POST'])
def queryMajor():
    year = request.form.get('year')
    dep_value = request.form.get('dep_value')
    term = request.form.get('term')
    grade = request.form.get('grade')
    major_list = analyse.getMajorListFor14(dep_value, year, term, grade)
    data = {
        "status":"",
        "data":{
            "major_list":""
        }
    }
    if not major_list:
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['major_list'] = major_list
    return json.dumps(data)

@app.route('/api/v1/queryClass', methods=['POST'])
def queryClass():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    class_id = request.form.get('class_id')[:12] if request.form.get('class_id') else ''
    grade = request.form.get('grade') if request.form.get('grade') else ''
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y',time.localtime(time.time())) )-1)
    term = request.form.get('term') if request.form.get('term') else '1'
    if (int(student_id[:4]) >= 2015):
        classList = analyse.getClassFor15(student_id, password, year, term)
    else:
        classList = analyse.getClassFor14(class_id, year, term, grade)
    data = {
        "status":"",
        "data":{
            "class_list":""
        }
    }
    if (classList == 'error'):
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['class_list'] = classList
    return json.dumps(data)


@app.route('/api/v1/queryExam', methods=['POST'])
def queryExam():
    student_id = request.form.get('student_id') if request.form.get('student_id') else ''
    password = request.form.get('password') if request.form.get('password') else ''
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y', time.localtime(time.time()))) - 1)
    term = request.form.get('term') if request.form.get('term') else '1'
    class_id = request.form.get('class_id')[:12] if request.form.get('class_id') else ''
    if (int(student_id[:4]) >= 2015):
        examList = analyse.getExamFor15(student_id, password, year, term)
    else:
        examList = analyse.getExamFor14(class_id)
    data = {
        "status":"",
        "data":{
            "exam_list":""
        }
    }
    if (examList == 'error'):
        data['status'] = False
        return json.dumps(data)
    data['status'] = True
    data['data']['exam_list'] = examList
    return json.dumps(data)


# Todo
@app.route('/api/v1/queryLib', methods=['POST'])
def queryLib():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    libList = analyse.getLib(student_id, password)
    if not libList:
        data = {
            "status":False,
            "data":"",
        }
    else:
        data = {
            "status":True,
            "data":libList
        }
    return json.dumps(data)


# Todo
@app.route('/api/v1/queryEcard', methods=['POST'])
def queryEcard():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    ecardInfo = analyse.getEcard(student_id, password)
    ecardInfo = json.loads(ecardInfo.text)
    if (ecardInfo['status'] == 200):
        data = {
            "status":True,
            "data":ecardInfo['data']
        }
    else:
        data = {
            "status":False,
            "data":"",
        }
    return json.dumps(data)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ ==  '__main__':
    app.run(port=8001)
