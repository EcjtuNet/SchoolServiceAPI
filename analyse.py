#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
import re
from login import Cas as cas
import config
from user import User

headers = config.get('headers')
login_url = config.get('login_url')
payload = config.get('payload')


# 智慧交大
def login_portal(username, password, info_url):
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


def getScoreInfoFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    url = "http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action"
    html = cas.page_by_get(cookie, headers, url)
    soup = BeautifulSoup(html, "lxml")
    originScoreInfoList = soup.find_all("ul", class_=year + '_' + term + " term_score")

    scoreInfoList = []
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
def getScoreInfoFor14(username, year, term):
    return


# Todo
def getStudentInfo():
    info_url = "http://portal.ecjtu.edu.cn/dcp/getPortalData?sPage=home&gId=null&user_id=null&cid=null&template_type=1"
    all_info = login_portal(info_url)
    print all_info
    return


# Todo
def testPassword():
    return


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

