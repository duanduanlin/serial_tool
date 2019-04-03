#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat a simple messagebox api-base version

---------------------
作者：追逐阳光的风
来源：CSDN
原文：https://blog.csdn.net/zhulove86/article/details/52524735
'''
__author__ = 'Duanlin D'

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMessageBox, QHBoxLayout, QLabel, QPushButton, QFrame

class MessageBox(QWidget):
    def __init__(self):
        super(MessageBox, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("MessageBox")
        self.setGeometry(400, 400, 300, 290)

        mainLayout = QHBoxLayout()
        self.displayLabel = QLabel("  ")
        self.displayLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        mainLayout.addWidget(self.displayLabel)
        self.setLayout(mainLayout)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("The property-base API")
        msgBox.setText("The Python file  has been modified.");
        msgBox.setInformativeText("Do you want to save your changes?");
        msgBox.setDetailedText("Python is powerful... and fast; \nplays well with others;\n \
           runs everywhere; \n is friendly & easy to learn; \nis Open.")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)

        ret = msgBox.exec()
        if ret == QMessageBox.Save:
            self.displayLabel.setText("Save")
        elif ret == QMessageBox.Discard:
            self.displayLabel.setText("Discard")
        elif ret == QMessageBox.Cancel:
            self.displayLabel.setText("Cancel")
        else:
            pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myshow = MessageBox()
    myshow.show()
    sys.exit(app.exec_())
