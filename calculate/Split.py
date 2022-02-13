from ui.SplitUI import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import pandas as pd
import tqdm
import math


class Split(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Excel Utils for choose v1.0')
        self.ui.loadButton.clicked.connect(self.__loadExcel)
        self.ui.sheetComboBox.activated[str].connect(self.__loadSheets)
        self.ui.splitButton.clicked.connect(self.__splitFields)
        self.ui.openButton.clicked.connect(self.__openFileDialog)
        self.ui.openButton_2.clicked.connect(self.__openFeeFile) #打开运费文件框
        self.ui.feeLoadButton.clicked.connect(self.__loadFeeExcel)
        self.ui.calTransFeeButton.clicked.connect(self.__calTransFee)

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
        path = self.ui.lineEdit.text()
        self.__dfs: dict = pd.read_excel(path, dtype=str, sheet_name=None)
        self.ui.sheetComboBox.addItems(list(self.__dfs.keys()))

    def __loadFeeExcel(self):
        path = self.ui.feeFilePathEdit.text()
        self.__feeDf = pd.read_excel(path, index_col='地区', dtype=str)
        QMessageBox.information(self, '成功', '运费已导入', QMessageBox.Yes, QMessageBox.Yes)

    def __calTransFee(self):
        weighField = self.ui.weighComboBox.currentText()
        addressField = self.ui.addressComboBox.currentText()

        lis = []
        for _, row in self.__df.iterrows():
            add = row[addressField].split()[0][:2]
            try:
                wei = float(row[weighField])
                if math.isnan(wei):
                    fee = 0
                else:
                    if wei > 0.5:
                        wei = math.ceil(float(row[weighField]))
                    if wei <= 0.5:
                        level = '0.5档'
                    elif wei <= 1:
                        level = '1档'
                    elif wei <= 2:
                        level = '2档'
                    elif wei <= 3:
                        level = '3档'
                    else:
                        level = 'depends'
                    info = self.__feeDf.loc[add, level]
                    fee = eval(info)
            except Exception as e:
                fee = 999999
            lis.append(fee)
        self.__df = pd.concat([self.__df, pd.Series(data=lis, name='运费自动计算')], axis=1)
        self.__df.to_excel('运费生成.xlsx', index=False)
        QMessageBox.information(self, '成功', '运费已计算完成', QMessageBox.Yes, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mydlg = Split()
    mydlg.show()
    sys.exit(app.exec_())