import pandas as pd

df:pd.DataFrame = pd.read_excel('计算.xlsx')
total = pd.DataFrame()

for idx, row in df.iterrows():
    dh = row['原始单号']
    zy = row['货品摘要']
    lis = zy.split(',')
    curRes = []
    for l in lis:
        curRes.append({'原始单号': dh, '货品': l[:l.rfind('*')], '数量': l[l.rfind('*')+1:]})
    print(curRes)
    total = total.append(curRes, ignore_index=True)

total.to_excel('res.xlsx', index=False)