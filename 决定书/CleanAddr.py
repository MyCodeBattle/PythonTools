import pandas as pd
import requests
from lxml import etree
import re
from loguru import logger
import time


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def get_html(province, baseUrl: str):
    proxys = {'http': 'http://localhost:4780'}
    for n in range(0, 10):
        time.sleep(0.2)
        if n == 0:
            url = baseUrl
        else:
            url = baseUrl + f'index_{n}.html'
        print(url)
        uhtml = requests.get(url, proxies=proxys)
        uhtml.encoding = 'utf-8'
        hrefs = etree.HTML(uhtml.text).xpath('//div[@class="fl_list"]//li//a/@href')
        for href in hrefs:
            url = baseUrl + href[1:]
            time.sleep(0.5)
            page = requests.get(url, proxies=proxys)

            page.encoding = 'utf-8'
            infoDic = resolve_title(page.text, province)
            if not infoDic:
                continue
            if infoDic['title'] != 'null' and '2019' in infoDic['date']:
                return


def resolve_title(text, source):
    html = etree.HTML(text)
    if '市场禁入决定书' in text:
        logger.info('不要市场禁入')
        return
    if '正文见附件' in text:
        logger.info('不要pdf')
        return

    # print(text)
    try:
        s = html.xpath('//div[@class="content"]//text()')
        while not is_chinese(s[-1]):
            s = s[:-1]
        words = ''.join(s)
        words = words.replace('\n\n', '')
        words = words.replace(' ', '')

        #解析标题
        tup: str = re.findall('[我本][局会](依法)*对(当事人)*(.*)(行为|案)进行', words)[0][2].strip()
        if tup[-1] == '的':
            tup = tup[:-1]
        if tup.find('（') != -1:
            tup = tup[:tup.find('（')] + tup[tup.find('）') + 1:]
        if len(tup) >= 50:
            tup = tup[:20] + '...'


        #解析日期
        date = re.findall(r'\d{4}年\d.*月.*日', words)[-1]
        logger.info(date)
        with open(f'决定书/{source}-{tup}-{date}.txt', 'w') as fp:
            fp.write(words)
    except Exception as e:
        logger.error(words)
        print(words)
        return {'title': 'null', 'date': 'null'}

    return {'title': tup, 'date': date}


def get_zjh_html():
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

    for page in range(1, 10):
        params = {'schn': 3313, 'year': 2021, 'sinfo': 3300, 'countpos': 1, 'curpos': '行政处罚决定', 'page': page}
        url = 'http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp'
        res = requests.post(url, data=params, headers=headers)
        html = etree.HTML(res.text)
        if '请注意您的检索词拼写' in html:
            logger.info('已经没内容了')
            return

        hrefs = html.xpath('//li[@class="mc"]/div/a/@href')
        baseUrl = 'http://www.csrc.gov.cn'
        for href in hrefs:
            url = baseUrl + href
            page = requests.get(url)
            page.encoding = 'utf-8'
            infoDic = resolve_title(page.text, '证监会')
            if infoDic['title'] != 'null' and '2019' in infoDic['date']:
                return


if __name__ == '__main__':

    url = 'http://www.csrc.gov.cn/pub/shanghai/xzcf/202106/t20210628_400415.htm'
    # a = requests.get(url)
    # a.encoding = 'utf-8'
    # text = a.text
    zjhs = [['青海', 'http://www.csrc.gov.cn/pub/qinghai/qhxzcf/'], ['新疆', 'http://www.csrc.gov.cn/pub/xinjiang/xjxzcf/'], ['深圳', 'http://www.csrc.gov.cn/pub/shenzhen/xzcf/'], ['大连', 'http://www.csrc.gov.cn/pub/dalian/dlxzcf/'], ['厦门', 'http://www.csrc.gov.cn/pub/xiamen/xmxzcf/'], ['青岛', 'http://www.csrc.gov.cn/pub/qingdao/xzcf/']]
    for area in zjhs:
        get_html(area[0], area[1])
    # get_zjh_html()


