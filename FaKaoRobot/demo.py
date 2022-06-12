from wxauto import *
import time
import robot

class FrontCodes:

    def __init__(self):
        self.wx = WeChat()
        self.wx.GetSessionList()
        self.__robot = robot.Robot()

        self.__isShuati = False
        self.__ques = None
        self.__isRead = set()

    def __sendMsg(self, msg):
        WxUtils.SetClipboard(msg)  # 将内容复制到剪贴板，类似于Ctrl + C
        self.wx.SendClipboard()  # 发送剪贴板的内容，类似于Ctrl + V

    def __getQuestion(self):
        self.__ques = self.__robot.random()
        self.__sendMsg(self.__ques['题干'])
        self.__sendMsg(self.__ques['选项'])

    def __isAnswerQuestion(self, msgs):
        '''
        判断是否在回答问题，如果只有英文字母就算是
        :param msgs:
        :return:
        '''

        for m in msgs:
            if not m.isalpha():
                return False
        return True

    def __judge(self, name: str, msgs: str):
        print(msgs)
        if '我要刷题' in msgs:
            if self.__isShuati: #如果有正在进行的刷题，忽略
                self.__sendMsg(f'@{name} 现在有正在进行的刷题！')
                return

            self.wx.SendMsg('刷题开始！')
            self.__getQuestion()
            self.__isShuati = True

        elif msgs.isalpha():
            if not self.__isAnswerQuestion(msgs):
                return
            if self.__robot.checkAns(msgs):
                self.__sendMsg(f'@【{name}】回答正确！答案为{self.__ques["答案"]}！五秒后进入下一题')
                time.sleep(5)
                self.__getQuestion()
                return


    def run(self):
        # 获取当前微信客户端


        # 获取会话列表

        msg = '大家好我是刷题机器人~'
        who = '加油法考人'
        # self.wx.ChatWith(who)  # 打开`文件传输助手`聊天窗口
        self.wx.SendMsg(msg)  # 向`文件传输助手`发送消息：你好~

        # 输出当前聊天窗口聊天消息
        old = ''
        while True:
            ## 获取更多聊天记录

            msgs = self.wx.GetLastMessage
            if msgs[2] in self.__isRead:
                continue
            self.__judge(msgs[0], msgs[1])
            self.__isRead.add(msgs[2])
            time.sleep(0.05)


        # 向某人发送消息（以`文件传输助手`为例）

if __name__ == '__main__':
    a = FrontCodes()
    a.run()