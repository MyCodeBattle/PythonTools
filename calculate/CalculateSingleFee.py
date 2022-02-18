#%%

import pandas as pd
import numpy as np
import sympy as sp
from loguru import logger
import traceback

df: pd.DataFrame = pd.read_excel('MergeName.xlsx', dtype={'快递单号': str})
comboDf = pd.read_excel('组合编号.xlsx')


# SDHY260g-1P*1

#%%

def nameFilter(s: str):
    global cnt
    no = s[:s.find('-')]
    if '*' not in s:
        s += '*1'
    num1 = int(s[s.find('-') + 1:s.find('*') - 1])
    num2 = int(s[s.find('*') + 1:])
    return no, num1*num2
    # print(f'no = {no}, num1 = {num1}, num2 = {num2}')



lis = []
for _, row in df.iterrows():
    ss = row['商家编码']
    if ss[:ss.find('*')] in comboDf['商品编码'].values:
        ss = comboDf[comboDf['商品编码'] == ss[:ss.find('*')]]['入库编码-组合拆分'].values
        ss = '*1,'.join(ss)
    ss = ss.replace(';', ',').replace(':', ',').replace('+', ',').split(',')

    total = 0
    for s in ss:
        try:
            tup = nameFilter(s)
            if tup[0] in dic:
                total += dic[tup[0]] * tup[1]
        except Exception as e:
            print(s)
            print(e)
    lis.append(total)

df['测算重量'] = lis
df.to_excel('测算上个月.xlsx', index=False)
print(dic)

