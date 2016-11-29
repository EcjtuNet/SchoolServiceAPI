#!/usr/bin/env python
# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re

import config


# 统一认证类
class Cas:
    def __init__(self):
        return

    @classmethod
    def get_lt_value(self, headers, login_url):
        cas_page = requests.get(login_url, headers=headers)
        soup = BeautifulSoup(cas_page.text, "lxml")
        lt_value = soup.find("input", {"name": "lt"}).get('value')
        return lt_value

    @classmethod
    def get_ticket_url(self, headers, login_url, payload, encodedService, service, username, password, lt):
        payload["encodedService"] = encodedService
        payload['service'] = service
        payload['username'] = username
        payload['password'] = self.hash_password(self, password)
        payload['lt'] = lt

        ticket_page = requests.post(login_url, data=payload, headers=headers).text
        pattern = re.findall(ur'\s\swindow\.location\.href="(.*)"\+cookie', ticket_page)
        if (len(pattern) == 0):
            return 'error'
        ticket_url = pattern[0]
        return ticket_url

    @classmethod
    def get_login_cookie(self, ticket_url, headers):
        if (isinstance(ticket_url, (str))):
            return 'error'
        page = requests.get(ticket_url, headers=headers, allow_redirects=False)
        return page.cookies

    @classmethod
    def page_by_get(self, cookies , headers, info_url):
        if (isinstance(cookies, (str))):
            return 'error'
        info_page = requests.get(info_url, cookies=cookies, headers=headers)
        return info_page.text

    @classmethod
    def page_by_post(self, cookies , headers, info_url, payload):
        if (isinstance(cookies, (str))):
            return 'error'
        info_page = requests.post(info_url, data=payload, cookies=cookies, headers=headers)
        return info_page.text

    @staticmethod
    def hash_password(self, password):
        encode_password = requests.get(config.get('node_server_url'),{"password": password})
        return encode_password

# 老版教务处类