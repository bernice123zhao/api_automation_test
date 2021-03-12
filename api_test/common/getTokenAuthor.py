from api_test.models import *
import requests
from selenium import webdriver
from urllib.parse import urlencode
import traceback
import datetime
from threading import Thread
import time
# def getToken(url,username,password):#qingqing
#     print(username)
#     print(password)
#     print(url)
#     co = webdriver.ChromeOptions()
#     co.headless = True  # 设置浏览器为无头模式
#     driver = webdriver.Chrome(options=co)
#     driver.get(url)
#     ReturnUrl = driver.find_element_by_xpath('//*[@id="ReturnUrl"]').get_attribute('value')
#     RequestVerificationToken = driver.find_element_by_xpath('//*[@id="login"]/input[3]').get_attribute('value')
#     diccookie = driver.get_cookies()
#     cookies = '.AspNetCore.Antiforgery.fNjqMEcPLWI=' + diccookie[0]['value']
#     driver.quit()
#     headers = {"Cookie": cookies}
#     data = {"ReturnUrl": ReturnUrl,
#             "code": "",
#             "Username": username,
#             "Password": password,
#             "button": "login",
#             "__RequestVerificationToken": RequestVerificationToken,
#             }
#     parameter = {
#         "returnUrl": ReturnUrl
#     }
#     data2 = urlencode(parameter)
#     s = requests.Session()
#     loginUrl = 'http://sso.qa.changingedusys.com/account/login?' + data2
#     r = s.post(loginUrl, headers=headers, data=data, allow_redirects=True)
#     # print(r.text)
#     Location = r.history[1].headers['Location']
#     token = txt_wrap_by('access_token=', '&token_type', Location)
#     print('获取成功Token')
#     Token='Bearer '+token
#     return Token

def getToken(url,username,password):#qingqing
    print(username)
    print(password)
    print(url)
    headers={"Content-Type":"application/json;charset=UTF-8"}
    data={"username":username,"password":password}
    r = requests.post(url, headers=headers, json=data, allow_redirects=True)
    print(r.text)
    token = r.json()["data"]["key"]
    Token='Token '+token    # 生成token的值
    print(Token)
    return Token


def txt_wrap_by(start_str, end, html):  # 截取两个字符串之间得值
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def async1(f):  # 异步调用
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@async1
def getTokenAuthor():
    obm = GlobalHost.objects.all().values()
    nowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for i in obm:
        try:
            username = i["username"]
            if username:
                password = i["password"]
                url = i["url"]
                id = i["id"]
                token_value=getToken(url,username,password)
                print("globalhost表的主键id：%s"%id)
                GlobalHost.objects.filter(id=id).update(value=token_value,LastUpdateTime=nowTime,key='Authorization')   # 设置的公用token、authorization
            else:
                pass
        except:
            print(traceback.print_exc())
            pass

if __name__ == '__main__':
    url = "http://127.0.0.1:8000/api/user/login"
    username = "admin"
    password = "admin123456"
    token_value = getToken(url, username, password)
    print("token的值：%s"%token_value)