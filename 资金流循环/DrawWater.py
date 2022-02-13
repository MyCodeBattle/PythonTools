from graphviz import Digraph
import pandas as pd
from loguru import logger


class DrawWater:
    def __init__(self):
        self.__totalEdges = {}
        self.__visit = set()
        self.__color = {}
        self.__stack = []
        self.__dfn = {}
        self.__low = {}
        self.__groupEdges = {}  # 大组的边情况
        self.__groupMap = {}    # 分组情况
        self.__df = None
        self.__idx = 1

    def __Tarjan(self, node):
        self.__visit.add(node)
        self.__stack.append(node)
        self.__dfn[node] = self.__idx
        self.__low[node] = self.__idx
        self.__idx += 1
        if node in self.__groupEdges:
            for nextNode in self.__groupEdges[node]:
                if nextNode == node:
                    continue

                if nextNode not in self.__dfn:  # 没有访问过
                    self.__Tarjan(nextNode)
                    self.__low[node] = min(self.__low[node], self.__low[nextNode])
                elif nextNode in self.__visit:
                    self.__low[node] = min(self.__low[node], self.__low[nextNode])

        if self.__dfn[node] == self.__low[node]:
            while True:
                now = self.__stack[-1]
                self.__color[now] = node
                self.__stack.pop()
                self.__visit.remove(now)
                if now == node:
                    break

    def __readRelatedCompany(self):
        self.__df = pd.read_excel('测试流水.xlsx', sheet_name=None)
        df = self.__df['关联关系']
        for idx, row in df.iterrows():
            u = row['主公司']
            v = row['关联公司']

            self.__groupMap.setdefault(u, u)
            self.__groupMap.setdefault(v, u)


    def run(self):
        self.__readRelatedCompany()

        g = Digraph('测试图片', comment='what')
        df = self.__df['资金流水']

        # 建边
        for idx, row in df.iterrows():
            fr = row['账户']
            to = row['对手方']
            jd = row['借贷标记']

            if jd == 'C':   # 如果是借，换方向
                fr, to = to, fr

            if fr not in self.__groupMap:
                self.__groupMap[fr] = fr    # 如果没关联关系，就一个人一组
            if to not in self.__groupMap:
                self.__groupMap[to] = to

            # 结点自己的边情况
            self.__totalEdges.setdefault(fr, set())  # 如果没出现过

            # 大组的边情况
            group = self.__groupMap[fr]
            if group not in self.__groupEdges:
                self.__groupEdges[group] = set()
                self.__color[group] = group

            curEdges = self.__totalEdges[fr]
            curGroupEdges = self.__groupEdges[group]

            groupTo = self.__groupMap[to]

            if to not in curEdges and fr != to:
                curEdges.add(to)

            if groupTo not in curGroupEdges and group != groupTo:
                curGroupEdges.add(groupTo)
        # logger.info(self.__groupEdges)
        # 找环

        for node in self.__groupEdges:
            if node not in self.__dfn:
                self.__Tarjan(node)

        logger.info(self.__color)
        for fr in self.__groupEdges:
            for to in self.__groupEdges[fr]:
                if self.__color[fr] == self.__color[to]:  # 去所有边表里找所有大组相同的边
                    for u in self.__totalEdges:
                        if self.__groupMap[u] == fr:
                            for v in self.__totalEdges[u]:
                                if self.__groupMap[v] == to:
                                    g.edge(u, v)

        g.view()


a = DrawWater()
a.run()
