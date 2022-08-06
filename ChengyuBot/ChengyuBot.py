#encoding: utf-8
from wxauto import *
import json
import time
from loguru import logger
import china_idiom as idiom

import china_idiom as cyBot

class FrontCodes:

    def __init__(self):
        self.wx = WeChat()
        self.wx.GetSessionList()

    def __sendMsg(self, msg):
        WxUtils.SetClipboard(msg)  # 将内容复制到剪贴板，类似于Ctrl + C
        self.wx.SendClipboard()  # 发送剪贴板的内容，类似于Ctrl + V

    def run(self):
        # 获取当前微信客户端

        # 获取会话列表

        # 输出当前聊天窗口聊天消息
        old = ''
        while True:
            ## 获取更多聊天记录

            msgs = self.wx.GetLastMessage
            if '拼音' in msgs[1]:
                lis = msgs[1].split()[0][3:]
                logger.debug(lis)
                words = lis
                print(words)
                ans = idiom.next_idioms_solitaire(words, 100)
                for a in ans:
                    if len(a) == 4:
                        self.__sendMsg(a)
                        break


            time.sleep(0.05)

        # 向某人发送消息（以`文件传输助手`为例）


if __name__ == '__main__':
    a = FrontCodes()
    a.run()