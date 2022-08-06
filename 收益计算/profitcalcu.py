import pandas as pd
import arrow
from loguru import logger

df = pd.read_excel('data.xlsx')
df['日期'] = pd.to_datetime(df['日期'])

zhai = 40000
gu = 160000
camp = 200000
mode = 'low'
logger.info('初始为股债82')

prevInvestDate = None

for _, row in df.iterrows():
    if row['日期'] < pd.to_datetime('2013-1-1'):
        continue

    matchDays = arrow.get(row['日期']).shift(years=-10)

    matchDaysStr = matchDays.format('YYYY-MM-DD')
    matchDaysDf = df[df['日期'] == matchDaysStr]
    while matchDaysDf.empty:
        matchDays = matchDays.shift(days=1)
        matchDaysStr = matchDays.format('YYYY-MM-DD')
        matchDaysDf = df[df['日期'] == matchDaysStr]
    calDf: pd.DataFrame = df.iloc[matchDaysDf.index[0]:_ + 1, ]
    todayPos = (1 - calDf['比例'].rank(method='average') / calDf.shape[0]).values[-1]

    profToday = (1 + (calDf['点位'].values[-1] - calDf['点位'].values[-2]) / calDf['点位'].values[-2])
    camp = camp * (1 + (calDf['点位'].values[-1] - calDf['点位'].values[-2]) / calDf['点位'].values[-2])
    gu = gu * (1 + (calDf['点位'].values[-1] - calDf['点位'].values[-2]) / calDf['点位'].values[-2])
    zhai = zhai * (1 + (0.06/365))
    # logger.info(f'{matchDaysStr}盈亏{profToday}')

    # if todayPos > 0.5:
    #     if mode == 'low':
    #         mode = 'middle'
    #         zichan = gu + zhai
    #         gu = zichan * 0.5
    #         zhai = zichan * 0.5
    #         logger.info(f'{row["日期"]}切换股债55')
    if todayPos >= 0.8:

        if mode == 'low':
            mode = 'high'
            zichan = gu + zhai
            zhai = zichan * 0.8
            gu = zichan * 0.2
            logger.info(f'{row["日期"]}切换股债28')
    if todayPos < 0.2:
        if mode == 'high':
            mode = 'low'
            zichan = gu + zhai
            zhai = zichan * 0.2
            gu = zichan * 0.8
            logger.info(f'{row["日期"]}切换股债82')

    if arrow.get(row['日期']).month != prevInvestDate:
        prevInvestDate = arrow.get(row['日期']).month

        # if mode == 'low':
        #     gu += 5000
        # else:
        #     zhai += 5000
        gu += 3000
        camp += 3000
        logger.debug(f'{prevInvestDate} 定投日')

logger.info(f'策略资产：{gu + zhai}，{matchDaysStr}, 一直持有资产：{camp}')
