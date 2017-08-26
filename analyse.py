#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
import re
import json
import requests

from login import Cas as cas
from login import Jwc as jwc
from login import Lib as lib
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

    ticket_url = cas.get_ticket_url(headers, login_url, payload,
                                    encodeService, service,
                                    username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    return login_cookie


# 教务系统
def login_jwxt(username, password):
    lt = cas.get_lt_value(headers, login_url)
    encodeService = "http%3a%2f%2fjwxt.ecjtu.jx.cn%2fstuMag%2fLogin_dcpLogin.action"
    service = "http://jwxt.ecjtu.jx.cn/stuMag/Login_dcpLogin.action"

    ticket_url = cas.get_ticket_url(headers, login_url, payload,
                                    encodeService, service,
                                    username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    return login_cookie


# 图书馆
def login_lib(username, password):
    lt = cas.get_lt_value(headers, login_url)
    encodeService = ""
    service = "http://lib.ecjtu.jx.cn/goldwsdl/login.aspx"

    ticket_url = cas.get_ticket_url(headers, login_url, payload,
                                    encodeService, service,
                                    username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    return login_cookie


# 一卡通
def login_ecard(username, password):
    lt = cas.get_ticket_url(headers, login_url)
    encodeService = ""
    service = "http://ecard.ecjtu.jx.cn/hdjtdrPortalHome.action"
    ticket_url = cas.get_ticket_url(headers, login_url, payload,
                                    encodeService, service,
                                    username, password, lt)
    login_cookie = cas.get_login_cookie(ticket_url, headers)
    return login_cookie


# 实时测试密码正确性
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


# 存储边缘信息
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
    if (all_info == 'error'):
        return 'error'
    info = json.loads(all_info)['list'][0]['map']
    user = User.saveInfo(username, info.get('CARD_ID', ''),
                         info.get('BIRTHDAY', ''), info.get('MOBILE', ''))
    return user


# 获取所有15以后班级名单
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


# 获取所有14及以前班级名单（不需要使用）
def get_student_list_for_14():
    url = "http://jwc.ecjtu.jx.cn:8080/jwcmis/stuquery.jsp"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    # 获取学院部门
    departments = soup.find_all("select",{"name": "depart"})[0].find_all("option")
    depart_list = []
    for department in departments:
        depart_list.append([department["value"], department.string])

    # 排除部门垃圾数据
    ignorance = ['10', '14', '31', '40', '61']
    depart_list = filter(lambda x:(x in ignorance) == False, depart_list)  

    # 获取年级
    grades = soup.find_all("select", {"name": "nianji"})[0].find_all("option")
    grade_list = []
    for grade in grades:
        if(int(grade["value"]) <= 2014):
            grade_list.append(grade["value"])

    # 获取班级
    class_list = []
    for depart in depart_list:
        for grade in grade_list:
            payload = {
                "depart": depart[0],
                "nianji": grade,
            }
            html = requests.get(url, params=payload).text
            soup = BeautifulSoup(html, "lxml")
            classes = soup.find_all("select",{"name": "banji"})[0].find_all("option")[1:]
            for class_item in classes:
                class_id = class_item["value"]
                class_name = class_item.string
                class_list.append([class_id, class_name])
                payload = {
                    "banji": class_id,
                }
                html = requests.get(url, params=payload).text
                soup = BeautifulSoup(html, "lxml")
                tr = soup.find_all("tr")[1:]
                if tr:
                    for i in tr:
                        td = i.find_all("td")
                        print depart[1],td[1].text,grade,class_name,td[1].text,td[2].text,td[3].text,td[4].text
                        row = {
                            'department' : depart[1],
                            'grade': grade,
                            'class_name': class_name,
                            'student_name' : td[1].text,
                            'student_class_id' : td[2].text,
                            'student_id' : td[3].text,
                            'student_status' : td[4].text
                        }
    return


def getScoreFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    url = "http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action"
    html = cas.page_by_get(cookie, headers, url)
    if (html == 'error'):
        return 'error'
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


def getTodaySchedule(username, password, date):
    cookies = login_jwxt(username, password)
    todaySchedule_url = 'http://jwxt.ecjtu.jx.cn/Schedule/Weekcalendar_getTodayWeekcalendar.action'
    todaySchedule_postdata = {'date': date,
                              'dataType': "json"}
    schedule_data = requests.post(todaySchedule_url, data=todaySchedule_postdata, cookies=cookies, headers=headers)
    data = json.loads(schedule_data.text)
    return data['weekcalendarpojoList']

def getScoreFor14(username, year, term):
    cookies = jwc.score_login()
    html = jwc.fetch_score(username, cookies, year, term)
    soup = BeautifulSoup(html, "lxml")

    result = soup.find_all("center")[1].__dict__
    result =  result['contents'][0]
    pattern = re.compile(r'\d+')
    r = pattern.findall(result)[0]
    if (int(r) == 0):
        return 'error'

    result = soup.find_all("tr")[2:]
    scoreList = []
    scoreInfoList = []
    for tr in result:
        td = tr.find_all("td")
        eleList = []
        for ele in td:
            contents = ele.__dict__
            content = contents['contents'][0]
            if (re.findall(r'red', content.encode('gbk'))):
                content = content.encode('gbk').replace('<font color="red">','')
                content = content.encode('gbk').replace('</font>','')
            eleList.append(content)
        scoreList.append(eleList)

    for originScoreInfo in scoreList:
        scoreInfo = {
            'objectName': originScoreInfo[3],
            'classRequirement': originScoreInfo[4],
            'assessment': None,
            'credit': originScoreInfo[5],
            'score': originScoreInfo[6]
        }
        scoreInfoList.append(scoreInfo)
    return scoreInfoList


def getClassFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    url = 'http://jwxt.ecjtu.jx.cn/Schedule/Schedule_getUserSchedume.action?term='+str(year)+'.'+str(term)
    html = cas.page_by_get(cookie, headers, url)
    if (html == 'error'):
        return 'error'
    soup = BeautifulSoup(html,"lxml")
    table = soup.find("table",class_="table_border",id="courseSche")
    trList = table.find_all('tr')
    classInfoList = []
    for i in [1,2,3,4,5,6]:
        originClassInfo = trList[i].find_all('td')
        singleClassInfoList = []
        for j in [1,2,3,4,5,6,7]:
            singleClassInfo = []
            a = originClassInfo[j].get_text("|", strip=True).split('|')
            if len(a[0]) > 0:
                if len(a) < 3:
                    singleClassInfo = [
                        {
                            "class_name": a[0],
                            "class_teacher": a[1].split(' ')[0],
                            "class_room": None,
                            "class_week": a[1].split(' ')[1],
                            "class_type": None,
                            "class_time": a[1].split(' ')[2]
                        }
                    ]
                elif len(a) > 3:
                    singleClassInfo = [
                        {
                            "class_name": a[0],
                            "class_teacher": a[1].split(' ')[0],
                            "class_room": a[1].split(' ')[1],
                            "class_week": a[2].split(' ')[0][:-3],
                            "class_type": a[2].split(' ')[0][-3:-1],
                            "class_time": a[2].split('  ')[1]
                        },
                        {
                            "class_name": a[3],
                            "class_teacher": a[4].split(' ')[0],
                            "class_room": a[4].split(' ')[1],
                            "class_week": a[5].split(' ')[0][:-3],
                            "class_type": a[5].split(' ')[0][-3:-1],
                            "class_time": a[5].split('  ')[1]
                        }
                    ]
                else:
                    singleClassInfo = [
                        {
                        "class_name": a[0],
                        "class_teacher": a[1].split(' ')[0],
                        "class_room": a[1].split(' ')[1],
                        "class_week": a[2].split(' ')[0],
                        "class_type": None,
                        "class_time": a[2].split('  ')[1]
                        }
                    ]
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


def getDepartmentListFor14():
    html = jwc.fetch_class_page()
    soup = BeautifulSoup(html, "lxml")
    departments = soup.find_all("select",{"name": "depart"})[0].find_all("option")
    depart_list = []
    for department in departments:
        depart_list.append({"dep_name": department.string, "dep_value": department["value"]})
    return depart_list



def getMajorListFor14(dep_value, grade):
    html = jwc.fetch_major_list(dep_value, grade)
    soup = BeautifulSoup(html, "lxml")
    majors = soup.find_all("select",{"name": "banji"})[0].find_all("option")[1:]
    major_list = []
    for major in majors:
        major_list.append({"major_name": major.string, "major_value": major["value"]})
    return major_list


def getClassFor14(class_id, year, term, grade):
    html = jwc.fetch_class_list(class_id, year, term, grade)
    soup = BeautifulSoup(html, "lxml")
    row_classes_list = soup.find_all("tr")[1:]
    classInfoList = []
    for i in [0,1,2,3,4]:
        originClassInfo = row_classes_list[i].find_all('td')
        singleClassInfoList = []
        for j in [1,2,3,4,5,6,7]:
            a= originClassInfo[j].get_text("|", strip=True).split('|')
            singleClassInfo = {}
            if a[0]:
                singleClassInfo = {
                    "class_name": a[1],
                    "class_teacher": a[2].split(' ')[0],
                    "class_room": a[2].split(' ')[1],
                    "class_week": a[3].split(' ')[0]
                }
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


def getExamFor15(username, password, year, term):
    cookie = login_jwxt(username, password)
    queryTerm = str(year) + '.' + str(term)
    url = 'http://jwxt.ecjtu.jx.cn/examArrange/stuExam_stuQueryExam.action?term=' + queryTerm + '&userName=' + username
    html = cas.page_by_get(cookie, headers, url)
    if (html == 'error'):
        return 'error'
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="table_border")
    trList = table.find_all('tr')

    examInfoList = []
    for i in range(1, len(trList) - 1):
        tdList = trList[i].find_all('td')
        singleExamInfoList = []
        for j in range(8):
            singleExamInfoList = {
                'major_name': tdList[1].string,
                'major_type': tdList[2].string,
                'class_name': tdList[3].string,
                'total_student': tdList[4].string,
                'exam_week': tdList[5].string,
                'exam_time': tdList[6].string,
                'exam_place': tdList[7].string,
                'exam_number': tdList[8].string,
                'teacher':{
                    'main_teacher': {'name': None, 'dep': None},
                    'assist_teacher': {'name': None, 'dep': None}
                }
            }
        examInfoList.append(singleExamInfoList)

    return examInfoList


def getExamFor14(class_id):
    html = jwc.get_exam_list(class_id)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all("table")
    if len(table) == 1:
        return 'error'
    exams = table[1].find_all("tr")
    examInfoList = []
    for exam in exams:
        items = exam.find_all("td")
        singleExamInfoList = {
            'major_name': clean_exam(items[1]),
            'major_type': None,
            'class_name': clean_exam(items[0]),
            'total_student': None,
            'exam_week': clean_exam(items[3]),
            'exam_time': clean_exam(items[4]),
            'exam_place': clean_exam(items[5]),
            'exam_number': None,
            'teacher': {
                'main_teacher': {'name': clean_exam(items[6]), 'dep': clean_exam(items[7])},
                'assist_teacher': {'name': clean_exam(items[8]), 'dep': clean_exam(items[9])},
            }
        }
        examInfoList.append(singleExamInfoList)
    return examInfoList

def clean_exam(item):
    return item.find_all("font")[0].string

# Todo
def getLib(student_id, password):
    headers = {
         'render':'json',
         'clientType':'json',
    }
    data = {"map":{"method":"getBookInfo","params":{"javaClass":"java.util.ArrayList","list":[student_id,1,50]}},"javaClass":"java.util.HashMap"}
    recordList = requests.post('http://portal.ecjtu.edu.cn/dcp/jy/jyH5Mobile.action', data=json.dumps(data), headers=headers).text
    recordList = json.loads(recordList)["list"]

    result = []
    for i in recordList:
        print i
        result = {
            'bookID': i["map"]["TSMC"],
            'bookName': i["map"]["BZ"],
            'borrowDate': i["map"]["GHRQ"]["time"],
            'returnDate': i["map"]["GHRQ"]["time"]
        }

    # html = lib.login_lib(username, password)
    # print html
    # soup = BeautifulSoup(html,"lxml")
    # table = soup.find("table", id="DataGrid1")
    # print table
    return result

# Todo
def getEcard(student_id, password):
    ticket_url = login_ecard(student_id, password)
    ticket_patt = re.compile(r'http://ecard.ecjtu.jx.cn/hdjtdrPortalHome.action\?ticket=(.+)')
    ticket = ticket_patt.findall(ticket_url)[0]
    result = requests.get('http://api.ecjtu.org/home/ecard/ecardtoday/card/' + student_id + '/ticket/' + ticket)
    return result