import requests
import json
def getToken(url,username,password):#qingqing
    print(username)
    print(password)
    print(url)
    headers={"Content-Type":"application/json;charset=UTF-8"}
    data={"username":"admin","password":"jifeng123"}
    r = requests.post(url, headers=headers, json=data, allow_redirects=True)
    print(r.text)
    token = r.json()["data"]["key"]
    Token='Token '+token
    print(Token)
    return Token

getToken('http://172.22.7.87:8020/api/user/login','admin','jifeng123')