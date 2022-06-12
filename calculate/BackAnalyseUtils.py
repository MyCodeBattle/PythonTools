import traceback
from loguru import logger
import time
import pandas as pd
import requests
import json
import random

class BackAnalyseUtils:
    def __init__(self):
        self.__csrftoken = ''
        self.getCsrfToken()


    def getCsrfToken(self):
        session = requests.session()
        session.get('http://www.kuaidi100.com')
        self.__csrftoken = session.cookies['csrftoken']
        logger.success(f'获取token={self.__csrftoken}')

    def analyse(self, dh):
        '''
        主入口
        :param dh:
        :return:
        '''
        try:
            cent = self.getContent(str(dh))
            resp = json.loads(cent)
        except Exception as e:
            traceback.print_exc()
            logger.error('网络连接出现错误')
            return 'ERROR'
        if '退回妥投' in cent:
            return '已退回'
        if '查无结果' in cent:
            return '查无结果'

        return resp['message'] if not resp['data'] else resp['data'][0]['context']

    def getContent(self, postid):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
            "Connection": "keep-alive",
            "Cookie": f"csrftoken={self.__csrftoken}; Hm_lvt_22ea01af58ba2be0fec7c11b25e88e6c=1649206952; _adadqeqwe1321312dasddocTitle=kuaidi100; _adadqeqwe1321312dasddocReferrer=; _adadqeqwe1321312dasddocHref=; WWWID=WWW2B27155195638FE5528998620D355BC6; BAIDU_SSP_lcr=https://www.baidu.com/link?url=vDGVDrzPSEP5rrnKnZuQkKf3A28P_N1oU8mk-BvuRH358xLnQrcLi07nO1I1Bqn9&wd=&eqid=d195c04300632a6c00000003624ce6a2; Hm_lpvt_22ea01af58ba2be0fec7c11b25e88e6c=1649206961",
            "Host": "www.kuaidi100.com",
            "Referer": "https://www.kuaidi100.com/?from=openv",
            "sec-ch-ua": "'Not A;Brand';v='99', 'Chromium';v='100', 'Google Chrome';v='100'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "'Windows'",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"

        }

        response = requests.post("https://www.kuaidi100.com/autonumber/autoComNum?text=" + postid, headers=headers)
        typeReault = response.json()
        if typeReault['auto'][0]['comCode'] == 'youzhengguonei':
            typeReault['auto'][0]['comCode'] = 'EMS'    #强行替换成EMS

        params = {
            'type': typeReault['auto'][0]['comCode'],
            'postid': postid,
            'temp': "0." + self.random_number(18),
            'phone': ''
        }

        url = 'http://www.kuaidi100.com/query'

        res = requests.get(url, headers=headers, params=params)

        js = res.json()

        return json.dumps(js, ensure_ascii=False)


    def random_number(self, num2):
        list2 = []
        for number in range(num2):
            str2 = str(random.randint(0, 9))
            list2.append(str2)
        b = " ".join(list2).replace(" ", "")
        return b

if __name__ == '__main__':
    a = BackAnalyseUtils()
    # a.analyse('9869248262253')
    df = pd.read_excel('逆向退货费.xlsx', dtype=str)
    for dh in df['单号']:
        try:
            time.sleep(2)
            words = a.analyse(dh.strip())
            logger.error(words)
            if '退回妥投' in words:
                logger.info(f'单号：{dh}退回妥投')
        except Exception as e:
            logger.info(dh)
