#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat a simple pushbutton
'''
__author__ = 'Duanlin D'

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import sys

class PushButton(QWidget):
    def __init__(self):
        super(PushButton, self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("PushButton")
        self.setGeometry(400, 400, 300, 260)

        self.closeButton = QPushButton(self)
        self.closeButton.setText("Close")  # text
        self.closeButton.setIcon(QIcon("close.jpg")) #icon
        self.closeButton.setShortcut('Ctrl+D') #shortcut key
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setToolTip("Close the widget") #Tool tip
        self.closeButton.move(100, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PushButton()
    ex.show()
    sys.exit(app.exec_())
