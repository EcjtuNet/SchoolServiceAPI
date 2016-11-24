#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
from cas import Login as login
import config

headers = config.get('headers')
login_url = config.get('login_url')
payload = config.get('payload')
username  = config.get('student_id')
password = config.get('cas_password')


# 智慧交大
def login_portal(info_url):
    lt = login.get_lt_value(headers, login_url)
    encodeService = "http%3a%2f%2fportal.ecjtu.edu.cn%2fdcp%2findex.jsp"
    service = "http://portal.ecjtu.edu.cn/dcp/index.jsp"
    info_url = "http://portal.ecjtu.edu.cn/dcp/getPortalData?sPage=home&gId=null&user_id=null&cid=null&template_type=1"

    ticket_url = login.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
    login_cookie = login.get_login_cookie(ticket_url, headers)
    info_page = login.get_login(login_cookie, headers, info_url)
    return info_page


# 教务系统
def login_jwxt(info_url):
    lt = login.get_lt_value(headers, login_url)
    encodeService = "http%3a%2f%2fjwxt.ecjtu.jx.cn%2fstuMag%2fLogin_dcpLogin.action"
    service = "http://jwxt.ecjtu.jx.cn/stuMag/Login_dcpLogin.action"

    ticket_url = login.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
    login_cookie = login.get_login_cookie(ticket_url, headers)
    info_page = login.get_login(login_cookie, headers, info_url)
    return info_page


def getScoreInfoFor15(year, term):
    html = login_jwxt('http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action')
    print html
    year = '2015'
    soup = BeautifulSoup(html, "html.parser")
    originScoreInfoList = soup.find_all("ul", class_=year + '_' + term + " term_score")
    print originScoreInfoList

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

def getScoreInfoFor14(year, term):
    html = login_portal('http://')
    return