#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request
import time
import json
import analyse

app = Flask(__name__)

@app.route('/api/v1/scoreQuery', methods=['POST'])
def getScore():
    username = request.form.get('username')
    password = request.form.get('password')
    year = request.form.get('year') if request.form.get('year') else str(int(time.strftime('%Y',time.localtime(time.time())) )-1)
    term = request.form.get('term') if request.form.get('term') else '1'
    if (int(username[:4]) >= 2015):
        scoreList = analyse.getScoreInfoFor15(username, password, year, term)
    else:
        scoreList = analyse.getScoreInfoFor14(username, year, term)
    return json.dumps(scoreList)


# Todo
@app.route('api/v1/testPassword', methods=['POST'])
def testPassword():
    return


# Todo
@app.route('api/v1/getName', methods=['POST'])
def getName():
    return


# Todo
@app.route('api/v1/infoQuery', methods=['POST'])
def getInfo():
    return

if __name__ == '__main__':
    app.run()