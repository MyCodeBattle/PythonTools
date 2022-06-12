import pandas as pd
import random


class Robot:

    def __init__(self):
        self.__df = pd.read_excel('题库.xlsx')
        self.__question = None


    def random(self):
        shape = self.__df.shape[0]
        rnd = random.randint(1, shape)
        # rnd = 5
        self.__question = self.__df.iloc[rnd]
        return self.__question

    def checkAns(self, ans:str):
        if ''.join(sorted(ans.strip().upper())) == self.__question['答案']:
            return True
        return False


if __name__ == '__main__':
    a = Robot()
    ques = a.random()