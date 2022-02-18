import pandas as pd

df = pd.read_excel('/Users/zhuolx/Downloads/电商计算/东莞快递费.xlsx', index_col='地区')

s = df.loc['中通', ]

dic = {'1档': 2.0, '2档': 2.7, 'depends': '2+(wei*2.4)'}
ss = pd.DataFrame(data=dic, index=['ins'])
print(pd.concat([df, ss]))