import hashlib
import json
import difflib
import requests
import time

timestamp = str(int((time.time())))
# print(timestamp)

token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
nonce = '123456789abcdefg'
passid = 'zdww'
key = "3C502C97ABDA40D0A60FBEE50FAAD1DA"


def get_zdwwsignature():
    zdwwsign = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + 'QkjjtiLM2dCratiA' + timestamp
    hsobj = hashlib.sha256()
    hsobj.update(zdwwsign.encode('utf-8'))
    zdwwsignature = hsobj.hexdigest().upper()
    # print(zdwwsignature)
    return zdwwsignature


def get_signatureheader():
    has256 = hashlib.sha256()
    sign_header = timestamp + token + nonce + timestamp
    has256.update(sign_header.encode('utf-8'))
    signatureHeader = has256.hexdigest().upper()
    # print(signatureHeader)
    return signatureHeader


def get_datas():
    url = 'https://bmfw.www.gov.cn/bjww/interface/interfaceJson'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # "Content-Length": "235",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "bmfw.www.gov.cn",
        "Origin": "http://bmfw.www.gov.cn",
        "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
        "x-wif-nonce": "QkjjtiLM2dCratiA",
        "x-wif-paasid": "smt-application",
        "x-wif-signature": get_zdwwsignature(),
        "x-wif-timestamp": timestamp
    }

    params = {
        'appId': "NcApplication",
        'paasHeader': "zdww",
        'timestampHeader': timestamp,
        'nonceHeader': "123456789abcdefg",
        'signatureHeader': get_signatureheader(),
        'key': "3C502C97ABDA40D0A60FBEE50FAAD1DA"
    }

    resp = requests.post(url, headers=headers, json=params)
    datas = resp.text
    return datas

get_datas()