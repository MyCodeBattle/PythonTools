from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import pandas as pd
import arrow
import sys

from UI.FxUI import Ui_MainWindow


class Compare(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('叶老师专用风险地区比对工具 v1.0')

        self.ui.preFilePushButton.clicked.connect(self.__openPreFileDialog)
        self.ui.nextFilePushButton.clicked.connect(self.__openNextFileDialog)
        self.ui.generateButton.clicked.connect(self.__compare)

    def showBox(self, msg):
        QMessageBox.information(self, '提示', msg, QMessageBox.Yes, QMessageBox.Yes)

    def __openPreFileDialog(self):
        '''
        打开前一天的文件框
        :return:
        '''
        files, _ = QFileDialog.getOpenFileName(self, '选择打开文件', '.', 'All Files (*);;Excel (*.xls)')
        self.ui.preFileLineEdit.setText(files)

    def __openNextFileDialog(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择打开文件', '.', 'All Files (*);;Excel (*.xls)')
        self.ui.nextFileLineEdit.setText(files)

    def __compare(self):
        '''
        对比
        :return:
        '''
        df1 = pd.read_excel(self.ui.preFileLineEdit.text(), dtype=str, skiprows=1)
        df2 = pd.read_excel(self.ui.nextFileLineEdit.text(), dtype=str, skiprows=1)

        df1['合并地址'] = df1['地级市'] + df1['县市区'] + df1['具体点位']
        df2['合并地址'] = df2['地级市'] + df2['县市区'] + df2['具体点位']

        df1['地址带政策'] = df1['地级市'] + df1['县市区'] + df1['具体点位'] + df1['健康管理措施']
        df2['地址带政策'] = df2['地级市'] + df2['县市区'] + df2['具体点位'] + df2['健康管理措施']
        changeDf = df2[df2['合并地址'].isin(df1['合并地址']) & (~df2['地址带政策'].isin(df1['地址带政策']))]

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

        writer = pd.ExcelWriter(f'{arrow.now().strftime("%m%d")}变化情况.xlsx')
        pd.DataFrame(increaseList).to_excel(writer, index=False, sheet_name='新增地区')
        pd.DataFrame(decreaseList).to_excel(writer, index=False, sheet_name='减少地区')
        pd.DataFrame(sameList).to_excel(writer, index=False, sheet_name='相同地区')
        changeDf.to_excel(writer, index=False, sheet_name='政策变化地区')

        writer.save()
        self.showBox('成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mydlg = Compare()
    mydlg.show()
    sys.exit(app.exec_())
