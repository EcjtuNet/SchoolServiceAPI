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
    year = request.form.get('year') if request.form.get('year') else time.strftime('%Y',time.localtime(time.time()))
    term = request.form.get('term') if request.form.get('term') else '1'
    scoreList = analyse.getScoreInfo(year, term)
    return json.dumps(scoreList)

if __name__ == '__main__':
    app.run()