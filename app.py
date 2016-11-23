#!/usr/bin/env python
# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import config

headers = config.get('headers')
login_url = config.get('login_url')
payload = config.get('payload')
username  = config.get('student_id')
password = config.get('cas_password')

class login:
    def __init__(self):
        return

    @classmethod
    def get_lt_value(this, headers, login_url):
        cas_page = requests.get(login_url, headers=headers)
        soup = BeautifulSoup(cas_page.text, "lxml")
        lt_value = soup.find("input", {"name": "lt"}).get('value')
        return lt_value

    @classmethod
    def get_ticket_url(this, headers, login_url, payload, encodedService, service, username, password, lt):
        payload["encodedService"] = encodedService
        payload['service'] = service
        payload['username'] = username
        payload['password'] = password
        payload['lt'] = lt

        ticket_page = requests.post(login_url, data=payload, headers=headers).text
        pattern = re.findall(ur'\s\swindow\.location\.href="(.*)"\+cookie', ticket_page)
        ticket_url = pattern[0]
        return ticket_url

    @classmethod
    def get_login_cookie(this, ticket_url, headers):
        page = requests.get(ticket_url, headers=headers, allow_redirects=False)
        return page.cookies

    @classmethod
    def get_login(this, cookies , headers, info_url):
        info_page = requests.get(info_url, cookies=cookies, headers=headers)
        return info_page.text

# portal
lt = login.get_lt_value(headers, login_url)
encodeService = "http%3a%2f%2fportal.ecjtu.edu.cn%2fdcp%2findex.jsp"
service = "http://portal.ecjtu.edu.cn/dcp/index.jsp"
info_url = "http://portal.ecjtu.edu.cn/dcp/getPortalData?sPage=home&gId=null&user_id=null&cid=null&template_type=1"

ticket_url = login.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
login_cookie = login.get_login_cookie(ticket_url, headers)
info_page = login.get_login(login_cookie, headers, info_url)
print info_page

# 教务系统
lt = login.get_lt_value(headers, login_url)
encodeService = "http%3a%2f%2fjwxt.ecjtu.jx.cn%2fstuMag%2fLogin_dcpLogin.action"
service = "http://jwxt.ecjtu.jx.cn/stuMag/Login_dcpLogin.action"
info_url = "http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action?item=0401"

ticket_url = login.get_ticket_url(headers, login_url, payload, encodeService, service, username, password, lt)
login_cookie = login.get_login_cookie(ticket_url, headers)
info_page = login.get_login(login_cookie, headers, info_url)
print info_page
