#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
import re
import json

from login import Cas as cas
import config
from user import User

headers = config.get('headers')
login_url = config.get('login_url')
payload = config.get('payload')


# 智慧交大
def login_portal(username, password):
    lt = cas.get_lt_value(headers, login_url)
    encodeService = "http%3a%2f%2fportal.ecjtu.edu.cn%2fdcp%2findex.jsp"
    service = "http://portal.ecjtu.edu.cn/dcp/index.jsp"

    ticket_url = cas.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    return login_cookie


# 教务系统
def login_jwxt(username, password):
    lt = cas.get_lt_value(headers, login_url)
    encodeService = "http%3a%2f%2fjwxt.ecjtu.jx.cn%2fstuMag%2fLogin_dcpLogin.action"
    service = "http://jwxt.ecjtu.jx.cn/stuMag/Login_dcpLogin.action"

    ticket_url = cas.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    return login_cookie


def testPassword(username, password):
    lt = cas.get_lt_value(headers, login_url)
    result = cas.get_ticket_url(config.get('headers'), login_url, payload,
                                encodedService="http%3a%2f%2fportal.ecjtu.edu.cn%2fdcp%2findex.jsp",
                                service="http://portal.ecjtu.edu.cn/dcp/index.jsp",
                                username=username,
                                password=password,
                                lt=lt
                                )
    return result


def saveStudentInfo(username, password):
    info_url = "http://portal.ecjtu.edu.cn/dcp/profile/profile.action"
    cookies = login_portal(username, password)
    headers = {
        'Content-Type' : 'application/json; charset=UTF-8',
        'User-Agent' : 'Mozilla/5.0(Macintosh;Intel Mac OSX 10_12_1) AppleWebKit 537.36(KHTML, like Gecko) Chrome 54.0.2840.98Safari537.36',
        'Referer' : 'http://portal.ecjtu.edu.cn/dcp/forward.action?path=/portal/portal&p=info',
        'Origin' : 'http: // portal.ecjtu.edu.cn',
        'render' : 'json',
        'clientType' : 'json'
    }
    payload = {
               "map":{
                    "method" : "getInfo",
                    "params" : None},
               "javaClass" : "java.util.HashMap"
              }
    all_info = cas.page_by_post(cookies, headers, info_url, json.dumps(payload))
    info = json.loads(all_info)['list'][0]['map']
    user = User.saveInfo(username, info.get('CARD_ID', ''), info.get('BIRTHDAY', ''), info.get('MOBILE', ''))
    return user


# 获取所有班级名单
def getStudentList(username, password):
    url = "http://jwxt.ecjtu.jx.cn/infoQuery/class_findClassList.action"
    cookie = login_jwxt(username, password)
    html = cas.page_by_get(cookie, headers, url)
    soup = BeautifulSoup(html, "lxml")
    # 获取学院
    departments = soup.find_all("select",{"name": "depInfo.departMent"})[0].find_all("option")
    departmentList = []
    for department in departments:
        departmentList.append(department["value"])
    # 获取年级
    grades = soup.find_all("select", {"name": "gra.grade"})[0].find_all("option")
    gradeList = []
    for grade in grades:
        if(int(grade["value"])>=2015):
            gradeList.append(grade["value"])
    # 获取班级
    for dep in departmentList:
        for gra in gradeList:
            payload = {
                "depInfo.departMent" : dep,
                "gra.grade" : gra,
                "classInfo.className" : "selectClass"
            }
            html = cas.page_by_post(cookie, headers, "http://jwxt.ecjtu.jx.cn/infoQuery/class_findClaByDepGra.action", payload)
            name_patt = re.compile(r'<option.+?>(.+?)</option>')
            class_names = name_patt.findall(html)[1:]
            value_patt = re.compile(r'<option\svalue=\'(.+?)\'>.+?</option>')
            class_value = value_patt.findall(html)[1:]
            class_dic = dict(zip(class_names, class_value))
            for key in class_dic:
                payload = {
                    "depInfo.departMent":dep,
                    "gra.grade":gra,
                    "classInfo.classID":class_dic[key]
                }
                html = cas.page_by_post(cookie, headers, "http://jwxt.ecjtu.jx.cn/infoQuery/class_findStuNames.action", payload)
                soup = BeautifulSoup(html, "lxml")
                tr = soup.find_all("tr", class_="classNameDis")
                for i in tr:
                    td = i.find_all("td")
                    info = {
                        'department' : dep,
                        'grade': gra,
                        'major': key,
                        'name' : td[1].text,
                        'sex' : td[2].text,
                        'class_id' : td[3].text,
                        'student_id' : td[4].text,
                        'student_status' : td[5].text
                    }
                    User.addUser(info)
    return


def getScoreFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    url = "http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action"
    html = cas.page_by_get(cookie, headers, url)
    scoreInfoList = []
    if (isinstance(html, (str))):
        return scoreInfoList
    soup = BeautifulSoup(html, "lxml")
    originScoreInfoList = soup.find_all("ul", class_=year + '_' + term + " term_score")

    for originScoreInfo in originScoreInfoList:
        item = originScoreInfo.find_all('li')
        scoreInfo = {
            'objectName': item[1].string,
            'classRequirement': item[2].string,
            'assessment': item[3].string,
            'credit': item[4].string,
            'score': item[5].string
        }
        scoreInfoList.append(scoreInfo)

    return scoreInfoList


# Todo
def getScoreFor14(username, year, term):
    return


def getClassFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    url = 'http://jwxt.ecjtu.jx.cn/Schedule/Schedule_getUserSchedume.action?term='+str(year)+'.'+str(term)
    html = cas.page_by_get(cookie, headers, url)
    soup = BeautifulSoup(html,"lxml")
    table = soup.find("table",class_="table_border",id="courseSche")
    trList = table.find_all('tr')
    classInfoList = []
    for i in [1,2,3,4,5,6]:
        originClassInfo = trList[i].find_all('td')
        singleClassInfoList = []
        for j in [1,2,3,4,5,6,7]:
            singleClassInfo = originClassInfo[j].get_text().replace('</br>',' ')
            singleClassInfoList.append(singleClassInfo)
        classInfoList.append(singleClassInfoList)
    monday,tuesday,wednesday,thursday,friday,saturday,sunday = zip(*classInfoList)

    classInfo = {
        'monday':monday,
        'tuesday':tuesday,
        'wednesday':wednesday,
        'thursday':thursday,
        'friday':friday,
        'saturday':saturday,
        'sunday':sunday
    }
    return classInfo

# Todo
def getClassFor14(username, year, term):
    return


def getExamFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    queryTerm = str(year) + '.' + str(term)
    url = 'http://jwxt.ecjtu.jx.cn/examArrange/stuExam_stuQueryExam.action?term=' + queryTerm + '&userName=' + username
    html = cas.page_by_get(cookie, headers, url)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="table_border")
    trList = table.find_all('tr')

    examInfoList = []
    for i in range(1, len(trList) - 1):
        tdList = trList[i].find_all('td')
        singleExamInfoList = []
        for j in range(8):
            singleExamInfoList = {
                '课程名称': tdList[1].string,
                '课程性质': tdList[2].string,
                '班级名称': tdList[3].string,
                '学生人数': tdList[4].string,
                '考试周次': tdList[5].string,
                '考试时间': tdList[6].string,
                '考试地点': tdList[7].string
            }
        examInfoList.append(singleExamInfoList)

    return examInfoList


# Todo
def getExamFor16(username, year, term):
    return
