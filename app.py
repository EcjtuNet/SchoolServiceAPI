#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request
import time
import json

import analyse
from user import User

app = Flask(__name__)

@app.route('/api/v1/confirmName', methods=['POST'])
def confirmName():
    student_id = request.form.get('student_id')
    name = User.getName(student_id)
    return name[:-1]+"*"


@app.route('/api/v1/getName', methods=['POST'])
def getName():
    student_id = request.form.get('student_id')
    name = User.getName(student_id)
    return name


@app.route('/api/v1/savePassword', methods=['POST'])
def savePassword():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    result = analyse.testPassword(student_id, password)
    if (result == 'error'):
        return 'error'
    User.savePassword(student_id, password)
    return 'ok'


# Todo
@app.route('/api/v1/infoQuery', methods=['POST'])
def getInfo():
    return


@app.route('/api/v1/queryScore', methods=['POST'])
def getScore():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y',time.localtime(time.time())) )-1)
    term = request.form.get('term') if request.form.get('term') else '1'
    if (int(student_id[:4]) >= 2015):
        scoreList = analyse.getScoreInfoFor15(student_id, password, year, term)
    else:
        scoreList = analyse.getScoreInfoFor14(student_id, year, term)
    return json.dumps(scoreList)


if __name__ == '__main__':
    app.run()