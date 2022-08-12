import hashlib
import json
import difflib
import requests
import time

class WjjFXDQ:

    def __init__(self):
        self.timestamp = str(int((time.time())))
        # print(timestamp)

        self.token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
        self.nonce = '123456789abcdefg'
        self.passid = 'zdww'
        self.key = "3C502C97ABDA40D0A60FBEE50FAAD1DA"


    def get_zdwwsignature(self):
        zdwwsign = self.timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + 'QkjjtiLM2dCratiA' + self.timestamp
        hsobj = hashlib.sha256()
        hsobj.update(zdwwsign.encode('utf-8'))
        zdwwsignature = hsobj.hexdigest().upper()
        # print(zdwwsignature)
        return zdwwsignature


    def get_signatureheader(self):
        has256 = hashlib.sha256()
        sign_header = self.timestamp + self.token + self.nonce + self.timestamp
        has256.update(sign_header.encode('utf-8'))
        signatureHeader = has256.hexdigest().upper()
        # print(signatureHeader)
        return signatureHeader


    def get_datas(self):
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
            "x-wif-signature": self.get_zdwwsignature(),
            "x-wif-timestamp": self.timestamp
        }

        params = {
            'appId': "NcApplication",
            'paasHeader': "zdww",
            'timestampHeader': self.timestamp,
            'nonceHeader': "123456789abcdefg",
            'signatureHeader': self.get_signatureheader(),
            'key': "3C502C97ABDA40D0A60FBEE50FAAD1DA"
        }

        resp = requests.post(url, headers=headers, json=params)
        datas = resp.text
        return datas
