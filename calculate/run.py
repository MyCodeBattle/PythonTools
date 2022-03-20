import pandas as pd
dfs = pd.read_excel('/Users/zhuolx/Downloads/电商计算/模板/运费.xlsx', index_col='地区', sheet_name=None)
df = dfs['长沙仓']
print(df.columns)
print(df['wei<=0.5'].values[0])
wei = 0.6
