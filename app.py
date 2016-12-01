#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request
import time
import json

import analyse
from user import User

app = Flask(__name__)

# get开头接口取自数据库
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
    return 'ok'


@app.route('/api/v1/getInfo', methods=['POST'])
def getInfo():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    u = User.getInfo(student_id, password)
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
    return json.dumps(info)


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
    return json.dumps(scoreList)


@app.route('/api/v1/queryClass', methods=['POST'])
def queryClass():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y',time.localtime(time.time())) )-1)
    term = request.form.get('term') if request.form.get('term') else '1'
    if (int(student_id[:4]) >= 2015):
        classList = analyse.getClassFor15(student_id, password, year, term)
    else:
        classList = analyse.getClassFor14(student_id, year, term)
    return json.dumps(classList)


@app.route('/api/v1/queryExam', methods=['POST'])
def queryExam():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y', time.localtime(time.time()))) - 1)
    term = request.form.get('term') if request.form.get('term') else '1'
    if (int(student_id[:4]) >= 2015):
        examList = analyse.getExamFor15(student_id, password, year, term)
    else:
        examList = analyse.getExamFor14(student_id, year, term)
    return json.dumps(examList)

if __name__ == '__main__':
    app.run()