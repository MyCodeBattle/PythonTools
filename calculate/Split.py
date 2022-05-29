from ui.SplitUI import *
import time
import pathlib
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import pandas as pd
import tqdm
import math
import traceback
from loguru import logger
import arrow
import BackAnalyseUtils

class Split(QMainWindow):

    def showBox(self, msg):
        QMessageBox.information(self, '提示', msg, QMessageBox.Yes, QMessageBox.Yes)

    def showErrorBox(self, msg):
        QMessageBox.warning(self, '有问题', msg, QMessageBox.Yes, QMessageBox.Yes)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Excel Utils for choose v4.0 by zhuolx')
        self.ui.loadButton.clicked.connect(self.__loadExcel)
        self.ui.sheetComboBox.activated[str].connect(self.__loadSheets)
        self.ui.splitButton.clicked.connect(self.__splitFields)
        self.ui.openButton.clicked.connect(self.__openFileDialog)
        self.ui.openButton_2.clicked.connect(self.__openFeeFile) #打开运费文件框
        self.ui.feeLoadButton.clicked.connect(self.__loadFeeExcel)
        self.ui.totalCalculate.clicked.connect(self.__calTotalFee)
        self.ui.mergeNumberButton.clicked.connect(self.__mergeDh)   # 合并编码
        self.ui.backAnalyse.clicked.connect(self.__backAnalyse)

        self.__weighField = ''
        self.__addressField = ''
        
        self.__df = None
        self.__dfs = None
        self.__feeDfs = None    #运费模板
        self.__paperBoxFeeDfs = None    #包材
        self.__packFeeDfs = None  #人工
        self.__valueAddDfs = None   #加钱！

        self.INF = 9999999

    def __openFileDialog(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择打开文件', '.', 'All Files (*);;Excel (*.xls)')
        self.ui.lineEdit.setText(files)

    def __openFeeFile(self):
        dire = QFileDialog.getExistingDirectory(self, '打开文件夹', '.')
        self.ui.feeFilePathEdit.setText(dire)

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
        self.__df = self.__dfs[sht].fillna('')

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
            self.__dfs: dict = pd.read_excel(path, dtype={'订单编号': str, '原始单号': str, '纸箱型号': str}, sheet_name=None)
            self.ui.sheetComboBox.addItems(list(self.__dfs.keys()))
        except FileNotFoundError as e:
            QMessageBox.information(self, '错误', '文件不存在！', QMessageBox.Yes, QMessageBox.Yes)

    def __loadFeeExcel(self):
        '''
        导入运费、包材费、人工费
        :return:
        '''
        path = self.ui.feeFilePathEdit.text()
        self.__feeDfs = pd.read_excel(pathlib.Path(path).joinpath('运费.xlsx'),sheet_name=None, dtype=str)
        self.__paperBoxFeeDfs = pd.read_excel(pathlib.Path(path).joinpath('包材费.xlsx'), sheet_name=None, dtype=str)
        self.__packFeeDfs = pd.read_excel(pathlib.Path(path).joinpath('打包费.xlsx'), sheet_name=None, dtype=str)
        self.__valueAddDfs = pd.read_excel(pathlib.Path(path).joinpath('增值服务费.xlsx'), sheet_name=None, dtype=str)
        QMessageBox.information(self, '成功', '四个费用已导入', QMessageBox.Yes, QMessageBox.Yes)
        logger.success('费用导入成功...')

    def __calPaperBoxFee(self, row):
        '''
        计算包材
        :param row 处理的行
        :return:
        '''
        try:
            curFeeDf = self.__paperBoxFeeDfs[row['仓库']]
            ntype = row['纸箱型号']
            return float(curFeeDf[curFeeDf['类型'] == ntype]['费用'].values[0])
        except Exception as e:
            traceback.print_exc()
            self.showBox('可能存在型号为空的数据')
            return self.INF

    def __calDeliveryFee(self, row) -> float:
        '''
        北京加1块，上海加0.5块
        :return:
        '''
        try:
            curFeeDf = self.__valueAddDfs[row['仓库']]
            fee = 0
            add = row[self.__addressField].split()[0]
            if add in curFeeDf.columns:
                fee = curFeeDf[add].values[0]
            return float(fee)
        except Exception as e:
            traceback.print_exc()
            return self.INF

    def __calPackFee(self, row):
        '''
        打包费
        0-1 0.2
        1-2 0.3
        2-3 0.4
        3-20 0.5
        4件以上 每件加0.1
        :return:
        '''
        try:
            curFeeDf = self.__packFeeDfs[row['仓库']]

            cur = 0
            wei = math.ceil(float(row[self.ui.weighComboBox.currentText()]))
            quantity = int(row['货品数量'])

            for gap in curFeeDf.columns:
                if eval(gap):
                    info = eval(curFeeDf[gap].values[0])
                    cur += info
            return cur
        except Exception as e:
            traceback.print_exc()
            return self.INF

    def __calTransFee(self, row, addressField, weighField) -> int:
        '''
        计算快递费
        :param row: 当前处理的行
        :param addressField: 地址字段
        :param weighField: 重量字段
        :return: 快递费 int
        '''
        if not self.__feeDfs:
            self.showBox('运费文件为空，是不是忘了点载入了？')
            raise Exception('运费为空')

        add = row[addressField].split()
        if not add:     #有地址是空的
            return self.INF
        else:
            add = add[0][:2]
        # logger.info(row[addressField])

        area = row['仓库']
        expressCompany = row['物流公司']

        if '中通' in expressCompany:
            expressCompany = '中通'
        elif '极兔' in expressCompany:
            expressCompany = '极兔'
        else:
            expressCompany = '百世'

        curFeeDf = self.__feeDfs[area].set_index('地区')
        try:
            wei = float(row[weighField])
            # 东莞仓新疆12元

            if math.isnan(wei):
                fee = 0
            else:
                for gap in curFeeDf:
                    if eval(gap):
                        if add in curFeeDf.index:
                            info = curFeeDf.loc[add, gap]
                        elif expressCompany in curFeeDf.index:
                            info = curFeeDf.loc[expressCompany, gap]  # 东莞按快递公司算快递费
                        else:
                            self.showErrorBox('找不到地址对应的运费')
                            raise Exception('计算出错')

                fee = eval(info)
            return fee
        except Exception as e:
            QMessageBox.information(self, '失败', '计算运费出现问题', QMessageBox.Yes, QMessageBox.Yes)
            traceback.print_exc()
            return self.INF

    def __calTotalFee(self):
        '''
        计算快递费，具体条件写在excel里
        :return:
        '''
        self.__weighField = self.ui.weighComboBox.currentText()
        self.__addressField = self.ui.addressComboBox.currentText()

        l1 = []
        l2 = []
        l3 = []
        l4 = []
        ntotal = self.__df.shape[0]
        bar = tqdm.tqdm(total=ntotal, ncols=200)
        try:

            for _, row in self.__df.iterrows():
                transFee = paperBoxFee = packFee = valueAddFee = '-'
                if self.ui.isCalTransFee.isChecked():
                    transFee = self.__calTransFee(row, self.__addressField, self.__weighField)
                if self.ui.isCalPaperBoxFee.isChecked():
                    paperBoxFee = self.__calPaperBoxFee(row)
                if self.ui.isCalPackFee.isChecked():
                    packFee = self.__calPackFee(row)
                if self.ui.isCalValueAddFee.isChecked():
                    valueAddFee = self.__calDeliveryFee(row)

                l1.append(transFee)
                l2.append(paperBoxFee)
                l3.append(packFee)
                l4.append(valueAddFee)
                bar.update(1)
            apDf = pd.DataFrame({'运费计算': l1, '包材费计算': l2, '打包费计算': l3, '增值服务计算': l4})
            self.__df = pd.concat([self.__df, apDf], axis=1)
        except Exception as e:
            traceback.print_exc()
            return
        finally:
            bar.close()

        try:
            self.__df.to_excel(f'终极生成-{arrow.now().minute}.xlsx', index=False)
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

    def __backAnalyse(self):
        if self.__df is None:
            self.showErrorBox('文件未载入')
            return

        if '单号' not in self.__df.columns:
            self.showErrorBox('找不到单号字段')
            return
        bar = tqdm.tqdm(total=self.__df.shape[0], ncols=150)
        utils = BackAnalyseUtils.BackAnalyseUtils()
        ans = []
        for dh in self.__df['单号']:
            time.sleep(2)
            ans.append(utils.analyse(dh))
            bar.update(1)
        self.__df['退回分析'] = ans
        self.__df.to_excel(f'{pathlib.Path(self.ui.lineEdit.text()).stem}退回分析.xlsx', index=False)
        bar.close()
        self.showBox('分析完成！')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mydlg = Split()
    mydlg.show()
    sys.exit(app.exec_())
