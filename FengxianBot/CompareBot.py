import pandas as pd
import pathlib
import click

class CompareBot:
    def __init__(self):
        self.__prePath = '温州市对国内重点地区来温返温人员健康管理措施（截至2022年8月19日）.xlsx'
        self.__nextPath = '温州市对国内重点地区来温返温人员健康管理措施（截至2022年8月20日上午）.xlsx'

        pass

    # @click.command()
    # @click.option('--pre', required=True)
    # @click.option('--next', required=True)
    def run(self, pre, next):
        df1 = pd.read_excel(pre, dtype=str, skiprows=1)
        df2 = pd.read_excel(next, dtype=str, skiprows=1)

        df1['合并地址'] = df1['地级市'] + df1['县市区'] + df1['具体点位']
        df2['合并地址'] = df2['地级市'] + df2['县市区'] + df2['具体点位']

        df1Set = set(list(df1['合并地址']))
        df2Set = set(list(df2['合并地址']))

        increase = df2Set.difference(df1Set)
        decrease = df1Set.difference(df2Set)
        same = df1Set.intersection(df1Set)


        decreaseList = []
        increaseList = []
        sameList = []
        for _, row in df1.iterrows():
            if row['合并地址'] in decrease:
                decreaseList.append(row)
            elif row['合并地址'] in same:
                sameList.append(row)

        for _, row in df2.iterrows():
            if row['合并地址'] in increase:
                increaseList.append(row)

        writer = pd.ExcelWriter('0820变化情况.xlsx')
        pd.DataFrame(increaseList).to_excel(writer, index=False, sheet_name='新增地区')
        pd.DataFrame(decreaseList).to_excel(writer, index=False, sheet_name='减少地区')
        pd.DataFrame(sameList).to_excel(writer, index=False, sheet_name='相同地区')

        writer.save()

        print(same)


pre = '温州市对国内重点地区来温返温人员健康管理措施（截至2022年8月19日）.xlsx'
next = '温州市对国内重点地区来温返温人员健康管理措施（截至2022年8月20日上午）.xlsx'
a = CompareBot()
a.run(pre, next)

