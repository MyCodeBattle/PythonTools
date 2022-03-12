import pandas as pd

df: pd.DataFrame = pd.read_excel('/Users/zhuolx/Downloads/合并单号.xlsx', dtype=str)

gps = df.groupby('快递单号')
totalDf = []

for dh, curDf in gps:
    curDf['合计'] = curDf['商品名称'] + '*' + curDf['数量']
    curDf['合计编码'] = curDf['商品编码'] + '*' + curDf['数量']
    names = ','.join(curDf['合计'].values)
    no = ','.join(curDf['合计编码'].values)
    totalDf.append({'快递单号': dh, '货品摘要': names, '商家编码': no})


pd.DataFrame(totalDf).to_excel(f'合并货品和编码.xlsx', index=False)
