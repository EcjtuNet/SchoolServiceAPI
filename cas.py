#!/usr/bin/env python
# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re


class Login:
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