# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SplitUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 100, 113, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 100, 60, 16))
        self.label.setObjectName("label")
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(240, 100, 81, 31))
        self.openButton.setObjectName("openButton")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(330, 90, 121, 41))
        self.loadButton.setObjectName("loadButton")
        self.sheetComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.sheetComboBox.setGeometry(QtCore.QRect(120, 160, 104, 26))
        self.sheetComboBox.setObjectName("sheetComboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 160, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(250, 160, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(440, 160, 60, 16))
        self.label_4.setObjectName("label_4")
        self.snComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.snComboBox.setGeometry(QtCore.QRect(320, 160, 104, 26))
        self.snComboBox.setObjectName("snComboBox")
        self.thingComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.thingComboBox.setGeometry(QtCore.QRect(500, 160, 104, 26))
        self.thingComboBox.setObjectName("thingComboBox")
        self.splitButton = QtWidgets.QPushButton(self.centralwidget)
        self.splitButton.setGeometry(QtCore.QRect(610, 151, 121, 41))
        self.splitButton.setObjectName("splitButton")
        self.calTransFeeButton = QtWidgets.QPushButton(self.centralwidget)
        self.calTransFeeButton.setGeometry(QtCore.QRect(610, 230, 121, 41))
        self.calTransFeeButton.setObjectName("calTransFeeButton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 240, 60, 16))
        self.label_5.setObjectName("label_5")
        self.weighComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.weighComboBox.setGeometry(QtCore.QRect(120, 240, 104, 26))
        self.weighComboBox.setObjectName("weighComboBox")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 210, 111, 21))
        self.label_6.setObjectName("label_6")
        self.feeFilePathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.feeFilePathEdit.setGeometry(QtCore.QRect(180, 210, 113, 21))
        self.feeFilePathEdit.setObjectName("feeFilePathEdit")
        self.openButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.openButton_2.setGeometry(QtCore.QRect(320, 210, 81, 31))
        self.openButton_2.setObjectName("openButton_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(250, 240, 61, 21))
        self.label_7.setObjectName("label_7")
        self.addressComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.addressComboBox.setGeometry(QtCore.QRect(330, 240, 104, 26))
        self.addressComboBox.setObjectName("addressComboBox")
        self.feeLoadButton = QtWidgets.QPushButton(self.centralwidget)
        self.feeLoadButton.setGeometry(QtCore.QRect(420, 200, 121, 41))
        self.feeLoadButton.setObjectName("feeLoadButton")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(110, 190, 551, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(100, 280, 551, 16))
        self.label_9.setObjectName("label_9")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(100, 130, 551, 16))
        self.label_13.setObjectName("label_13")
        self.totalCalculate = QtWidgets.QPushButton(self.centralwidget)
        self.totalCalculate.setGeometry(QtCore.QRect(330, 310, 113, 91))
        self.totalCalculate.setObjectName("totalCalculate")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 792, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "路径"))
        self.openButton.setText(_translate("MainWindow", "打开"))
        self.loadButton.setText(_translate("MainWindow", "确认装载"))
        self.label_2.setText(_translate("MainWindow", "Sheets"))
        self.label_3.setText(_translate("MainWindow", "订单字段"))
        self.label_4.setText(_translate("MainWindow", "货品字段"))
        self.splitButton.setText(_translate("MainWindow", "切分"))
        self.calTransFeeButton.setText(_translate("MainWindow", "生成运费"))
        self.label_5.setText(_translate("MainWindow", "重量字段"))
        self.label_6.setText(_translate("MainWindow", "运费计算文件路径"))
        self.openButton_2.setText(_translate("MainWindow", "打开"))
        self.label_7.setText(_translate("MainWindow", "收货地址"))
        self.feeLoadButton.setText(_translate("MainWindow", "确认装载"))
        self.label_8.setText(_translate("MainWindow", "————————————————————————————————————————————————"))
        self.label_9.setText(_translate("MainWindow", "————————————————————————————————————————————————"))
        self.label_13.setText(_translate("MainWindow", "————————————————————————————————————————————————"))
        self.totalCalculate.setText(_translate("MainWindow", "混合计算"))
