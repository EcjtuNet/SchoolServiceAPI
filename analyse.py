#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
from login import Cas as cas
import config

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
    info_page = cas.get_login(login_cookie, headers, info_url)
    return info_page


# 教务系统
def login_jwxt(username, password, info_url):
    lt = cas.get_lt_value(headers, login_url)
    encodeService = "http%3a%2f%2fjwxt.ecjtu.jx.cn%2fstuMag%2fLogin_dcpLogin.action"
    service = "http://jwxt.ecjtu.jx.cn/stuMag/Login_dcpLogin.action"

    ticket_url = cas.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    info_page = cas.get_login(login_cookie, headers, info_url)
    return info_page


def getScoreInfoFor15(username, password, year, term):
    html = login_jwxt(username, password, 'http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action')
    soup = BeautifulSoup(html, "html.parser")
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


def getScoreInfoFor14(username, year, term):
    return


def getStudentInfo():
    info_url = "http://portal.ecjtu.edu.cn/dcp/getPortalData?sPage=home&gId=null&user_id=null&cid=null&template_type=1"
    all_info = login_portal(info_url)
    print all_info
    return
