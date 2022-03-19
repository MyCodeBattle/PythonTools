from ui.SplitUI import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import pandas as pd
import tqdm
import math
import traceback
from loguru import logger


class Split(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Excel Utils for choose v2.2')
        self.ui.loadButton.clicked.connect(self.__loadExcel)
        self.ui.sheetComboBox.activated[str].connect(self.__loadSheets)
        self.ui.splitButton.clicked.connect(self.__splitFields)
        self.ui.openButton.clicked.connect(self.__openFileDialog)
        self.ui.openButton_2.clicked.connect(self.__openFeeFile) #打开运费文件框
        self.ui.feeLoadButton.clicked.connect(self.__loadFeeExcel)
        self.ui.calTransFeeButton.clicked.connect(self.__calTransFee)
        self.ui.totalCalculate.clicked.connect(self.__calMuchFee)
        self.ui.mergeNumberButton.clicked.connect(self.__mergeDh)   # 合并编码
        
        self.__df = None
        self.__dfs = None

    def __calMuchFee(self):
        '''
        混合计算
        :return:
        '''

        self.__calPackFee()
        self.__calPaperBoxFee()
        self.__calDeliveryFee()
        self.__calTransFee()

    def __openFileDialog(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择打开文件', '.', 'All Files (*);;Excel (*.xls)')
        self.ui.lineEdit.setText(files)

    def __openFeeFile(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择打开文件', '.', 'All Files (*);;Excel (*.xls)')
        self.ui.feeFilePathEdit.setText(files)

    def __splitFields(self):
        total = pd.DataFrame()

        dhName = self.ui.snComboBox.currentText()   # 单号名称
        zyName = self.ui.thingComboBox.currentText()      # 货品详情名称
        with tqdm.tqdm(total=self.__df.shape[0]) as countBar:
            for idx, row in self.__df.iterrows():
                dh = row[dhName]
                zy = row[zyName]
                lis = zy.split(',')

                curRes = []
                for l in lis:
                    curRes.append({'原始单号': dh, '货品': l[:l.rfind('*')], '数量': l[l.rfind('*') + 1:]})

                total = total.append(curRes, ignore_index=True)
                countBar.update(1)

        total.to_excel('res.xlsx', index=False)
        QMessageBox.information(self, '成功', '文件已生成', QMessageBox.Yes, QMessageBox.Yes)

    def __loadSheets(self):
        sht = self.ui.sheetComboBox.currentText()
        self.__df = self.__dfs[sht]

        self.ui.snComboBox.clear()
        self.ui.thingComboBox.clear()
        self.ui.weighComboBox.clear()
        self.ui.addressComboBox.clear()
        self.ui.snComboBox.addItems(self.__df.columns)
        self.ui.thingComboBox.addItems(self.__df.columns)
        self.ui.weighComboBox.addItems(self.__df.columns)
        self.ui.addressComboBox.addItems(self.__df.columns)

    def __loadExcel(self):
        try:
            path = self.ui.lineEdit.text()
            self.__dfs: dict = pd.read_excel(path, dtype=str, sheet_name=None)
            self.ui.sheetComboBox.addItems(list(self.__dfs.keys()))
        except FileNotFoundError as e:
            QMessageBox.information(self, '错误', '文件不存在！', QMessageBox.Yes, QMessageBox.Yes)

    def __loadFeeExcel(self):
        path = self.ui.feeFilePathEdit.text()
        self.__feeDfs = pd.read_excel(path, index_col='地区', dtype=str)
        QMessageBox.information(self, '成功', '运费已导入', QMessageBox.Yes, QMessageBox.Yes)

    def __calPaperBoxFee(self):
        '''
        计算包材
        :return:
        '''
        logger.info('计算包材...')

        if '包材（五层纸箱）' in self.__df.columns:
            self.__df['计算包装'] = self.__df['包材（五层纸箱）'].replace({'4': 2.1, '5': 1.4, '6': 1.2, '7': 1, '8': 0.8, '9': 0.72, '10': 0.59, '11': 0.47, '12': 0.36})
            # TODO 替换包材费

    def __calDeliveryFee(self):
        '''
        北京加1块，上海加0.5块
        :return:
        '''
        logger.info('计算北京上海加钱...')

        self.__df['北京上海加钱'] = 0
        self.__df.loc[(self.__df['省市区'].str.startswith('北京')) & (self.__df['仓库'] == '长沙仓'), '北京上海加钱'] = 1
        self.__df.loc[(self.__df['省市区'].str.startswith('上海')) & (self.__df['仓库'] == '长沙仓'), '北京上海加钱'] = 0.5

    def __calPackFee(self):
        '''
        打包费
        0-1 0.2
        1-2 0.3
        2-3 0.4
        3-20 0.5
        4件以上 每件加0.1
        :return:
        '''
        logger.info('计算打包费...')

        lis = []
        cur = 99999
        for _, row in self.__df[['结算重量', '货品数量']].iterrows():
            wei = math.ceil(float(row['结算重量']))
            if wei <= 1:
                cur = 0.2
            elif wei <= 2:
                cur = 0.3
            elif wei <= 3:
                cur = 0.4
            else:
                cur = 0.5
            if int(row['货品数量']) > 3:
                cur += 0.1 * (int(row['货品数量']) - 3)
            lis.append(cur)
        self.__df['计算人工'] = lis

    def __calTransFee(self):
        weighField = self.ui.weighComboBox.currentText()
        addressField = self.ui.addressComboBox.currentText()

        lis = []
        for _, row in self.__df.iterrows():
            add = row[addressField].split()[0][:2]
            area = row['仓库']
            expressCompany = row['物流公司']
            if '中通' in expressCompany:
                expressCompany = '中通'
            elif '极兔' in expressCompany:
                expressCompany = '极兔'
            else:
                expressCompany = '百世'

            try:
                wei = float(row[weighField])
                # 东莞仓新疆12元

                if math.isnan(wei):
                    fee = 0
                else:
                    for gap in self.__df.columns:
                        if eval(gap):
                            if '东莞' not in area:
                                info = self.__feeDfs[area].loc[add, gap]
                            else:
                                info = self.__feeDf.loc[expressCompany, gap]    # 东莞按快递公司算快递费
                            break

                    fee = eval(info)
                    if '东莞' in area and add == '新疆':
                        fee = 12 * wei

            except Exception as e:
                traceback.print_exc()
                print(add)
                fee = 999999
            lis.append(fee)
        self.__df = pd.concat([self.__df, pd.Series(data=lis, name='运费自动计算')], axis=1)
        try:
            self.__df.to_excel('运费生成.xlsx', index=False)
        except Exception as e:
            QMessageBox.information(self, '失败', '文件写入失败', QMessageBox.Yes, QMessageBox.Yes)
            return
        QMessageBox.information(self, '成功', '运费已计算完成', QMessageBox.Yes, QMessageBox.Yes)

    def __mergeDh(self):
        '''
        合并单号和编码
        :return:
        '''

        try:
            c = self.__df.columns
        except Exception as e:
            QMessageBox.information(self, '错误', '要点一下需要加载的 Sheet！', QMessageBox.Yes, QMessageBox.Yes)
            return

        if '商品名称' not in c or '商品编码' not in c or '数量' not in c or '快递单号' not in c:
            QMessageBox.information(self, '错误', '请检查表内是否有「商品名称」、「商品编码」、「快递单号」、「数量」字段！', QMessageBox.Yes, QMessageBox.Yes)
            return

        gps = self.__df.groupby('快递单号')
        totalDf = []

        for dh, curDf in gps:
            curDf['合计'] = curDf['商品名称'] + '*' + curDf['数量']
            curDf['合计编码'] = curDf['商品编码'] + '*' + curDf['数量']
            names = ','.join(curDf['合计'].values)
            no = ','.join(curDf['合计编码'].values)
            totalDf.append({'快递单号': dh, '货品摘要': names, '商家编码': no})

        pd.DataFrame(totalDf).to_excel(f'合并货品和编码.xlsx', index=False)
        QMessageBox.information(self, '成功', '编码已合并完成！', QMessageBox.Yes, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mydlg = Split()
    mydlg.show()
    sys.exit(app.exec_())
