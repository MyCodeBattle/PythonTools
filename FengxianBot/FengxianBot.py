from dingtalkchatbot.chatbot import *
import json
from loguru import logger
import arrow
from retrying import retry
import os
import GetData
import requests


class FengxianBot:
    def __init__(self):

        with open('token.txt', 'r') as fp:
            lis = fp.readlines()
            token = lis[0].strip()
            token2 = lis[1].strip()

        self.url = f'https://openplatform-pro.ding.zj.gov.cn/robot/send?access_token={token}'
        self.url2 = f'https://openplatform-pro.ding.zj.gov.cn/robot/send?access_token={token2}'
        self.__bot = DingtalkChatbot(self.url)
        self.__bot2 = DingtalkChatbot(self.url2)
        pass

    def analyseArea(self, riskList):
        '''
        解析出风险地区的set
        :param riskStr
        :return:  set
        '''

        st = set()
        for area in riskList:
            if area['province'] == area['city']:
                area['city'] = ''
            if area['city'] == '省直辖县级行政单位':
                area['city'] = ''
            areaName = area['province'] + area['city'] + area['county']
            for c in area['communitys']:
                st.add(areaName + c)
        return st

    def fetchLatest(self):

        # cookies = {
        #     'Hm_lvt_ece58dbd46906f2a1a152da450de76ac': '1659762786',
        #     'Hm_lpvt_ece58dbd46906f2a1a152da450de76ac': '1659762786',
        # }
        #
        # headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        #     'Cache-Control': 'max-age=0',
        #     # Requests sorts cookies= alphabetically
        #     # 'Cookie': 'Hm_lvt_ece58dbd46906f2a1a152da450de76ac=1659762786; Hm_lpvt_ece58dbd46906f2a1a152da450de76ac=1659762786',
        #     'DNT': '1',
        #     'Proxy-Connection': 'keep-alive',
        #     'Referer': 'http://diqu.gezhong.vip/',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        # }
        #
        # response = requests.get('http://diqu.gezhong.vip/api.php', cookies=cookies, headers=headers, verify=False)
        dataBot = GetData.WjjFXDQ()
        self.__today = json.loads(dataBot.get_datas())
        highList = self.__today['data']['highlist']
        midList = self.__today['data']['middlelist']
        now = arrow.now()
        high = self.analyseArea(highList)
        mid = self.analyseArea(midList)

        with open(f'{now.month}月{now.day}日.txt', 'w') as fp:
            fp.write(str({'高风险': high, '中风险': mid}))
        return high, mid

    def __uploadAndSave(self, w1, w2, w3, w4):
        '''
        上传到在线文本文档
        :param w1:
        :param w2:
        :param w3:
        :param w4:
        :return: links
        '''

        files = {
            'format': (None, 'url'),
            'content': (None, f'{w1}+"\n\n"+{w2}+\n\n+{w3}+\n\n+{w4}+\n\n'),
            'lexer': (None, '_markdown'),
        }
        return requests.post('https://dpaste.org/api/', files=files).text

    @retry(wait_fixed=60 * 1000, stop_max_attempt_number=10)
    def entry(self):
        logger.info('进入执行程序...')
        todayHighRisk, todayMidRisk = self.fetchLatest()

        date = arrow.now().shift(days=-1)
        with open(f'{date.month}月{date.day}日.txt', 'r') as fp:
            yesMp = eval(fp.read())
            yesMidRisk = yesMp['中风险']
            yesHighRisk = yesMp['高风险']

        reduceMidRiskArea = '\n\n'.join(sorted(yesMidRisk.difference(todayMidRisk)))  # 减少的地区
        reduceHighRiskArea = '\n\n'.join(sorted(yesHighRisk.difference(todayHighRisk)))  # 减少的高风险地区
        increaseMidRiskArea = '\n\n'.join(sorted(todayMidRisk.difference(yesMidRisk)))  # 增加的中风险
        increaseHighRiskArea = '\n\n'.join(sorted(todayHighRisk.difference(yesHighRisk)))  # 增加的高风险

        words1 = '# 较昨日减少的高风险地区：\n'
        words1 += reduceHighRiskArea + '\n\n'
        # print(words)

        words2 = '# 较昨日减少的中风险地区：\n'
        words2 += reduceMidRiskArea + '\n\n'

        words3 = '# 较昨日增加的高风险地区：\n'
        words3 += increaseHighRiskArea + '\n\n'
        # print(words)

        words4 = '# 较昨日增加的中风险地区：\n'
        words4 += increaseMidRiskArea + '\n\n'

        links = self.__uploadAndSave(words1, words2, words3, words4)

        logger.debug(links)
        res = self.__bot.send_text(
            '每日风险地区动态播报：\n' + f'截至{self.__today["data"]["end_update_time"]}，今日新增高风险地区{len(todayHighRisk.difference(yesHighRisk))}个、中风险地区{len(todayMidRisk.difference(yesMidRisk))}个，今日减少高风险地区{len(yesHighRisk.difference(todayHighRisk))}个、中风险地区{len(yesMidRisk.difference(todayMidRisk))}个，详情参见{links.strip()}')

        self.__bot2.send_text(
            '每日风险地区动态播报：\n' + f'截至{self.__today["data"]["end_update_time"]}，今日新增高风险地区{len(todayHighRisk.difference(yesHighRisk))}个、中风险地区{len(todayMidRisk.difference(yesMidRisk))}个，今日减少高风险地区{len(yesHighRisk.difference(todayHighRisk))}个、中风险地区{len(yesMidRisk.difference(todayMidRisk))}个，详情参见{links.strip()}')
        logger.debug(res)

    def start(self):
        self.entry()
        while True:
            if (arrow.now().hour == 12 and arrow.now().minute == 0) or (
                    arrow.now().hour == 21 and arrow.now().minute == 0):
                self.entry()
            logger.info('活着')
            time.sleep(60)


if __name__ == '__main__':
    a = FengxianBot()
    a.start()
