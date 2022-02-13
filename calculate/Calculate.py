import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from qt.ui import *

class Calculate(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(None)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def show_text(self):
        print(self)
        self.ui.textEdit.setText('成功显示！')

    def clear_text(self):
        self.ui.textEdit.clear()
        self.ui.clearButton.setText('已清楚')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mydlg = Calculate()
    mydlg.show()
    sys.exit(app.exec_())
