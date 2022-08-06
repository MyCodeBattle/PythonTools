#!/usr/bin/env python
# encoding:utf-8

import china_idiom as cyBot
import random
import sys

data = []

class IdiomsRobot:

    def get_pinyin(self, word):
        pinyin = []
        for i in word:
            pinyin.append(hanzi2pinyin.hanzi2pinyin(i))
        return pinyin

    def get_all_starts_with(self, letter):
        result = []
        target_pinyin = self.get_pinyin(letter)
        target_pinyin_first = target_pinyin[-1]
        for i in data:
            data_word = i[0]
            data_pinyin = i[1]
            data_meaning = i[2]
            data_pinyin_first = data_pinyin[0]
            if data_pinyin_first == target_pinyin_first:
                result.append([data_word, data_meaning])
        return result


    def get_random_result(self, data):
        return random.choice(data)

    def format_data(self, data):
        return "[%s] : [%s]" % (data[0], data[1])

    def __init__(self):
        with open("data.txt", "r") as f:
            counter = 0
            for line in f:
                content = line.decode("UTF-8").split("\t")
                word = content[0]
                pinyin = content[1].split("'")
                meaning = content[2].replace("\n", "")
                data.append([word, pinyin, meaning])
                counter += 1

    def guess(self, word):
        all_data_matched = self.get_all_starts_with(word)
        result_data = self.format_data(self.get_random_result(all_data_matched))
        return result_data


if __name__ == '__main__':
    a = IdiomsRobot()
    print(a.guess('海阔天空'))