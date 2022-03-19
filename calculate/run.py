import pandas as pd
df = pd.read_excel('/Users/zhuolx/Downloads/运费.xlsx', index_col='地区', sheet_name=None)
print(df['旭昇'])
wei = 0.6
for c in df.columns:
    if c == '地区':
        continue
    if eval(c):
        print(df.loc['浙江', c])
