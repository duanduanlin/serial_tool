#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat a simple view table example

---------------------
作者：追逐阳光的风
来源：CSDN
原文：https://blog.csdn.net/zhulove86/article/details/52599738
'''
__author__ = 'Duanlin D'

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTableWidget,QHBoxLayout, QTableWidgetItem, QComboBox,QFrame
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap

class TableSheet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        horizontalHeader = ["工号", "姓名", "性别", "年龄", "职称"]

        self.setWindowTitle('TableWidget Usage')
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(2)
        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectColumns)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.table.setColumnWidth(4, 200)
        self.table.setRowHeight(0,40)
        #self.table.setFrameShape(QFrame.HLine)#设定样式
        #self.table.setShowGrid(False) #取消网格线
        #self.table.verticalHeader().setVisible(False) #隐藏垂直表头

        self.table.setItem(0, 0, QTableWidgetItem("001"))
        self.table.setItem(0, 1, QTableWidgetItem("Tom"))
        genderComb = QComboBox()
        genderComb.addItem("男性")
        genderComb.addItem("女性")
        genderComb.setCurrentIndex(0)
        self.table.setCellWidget(0, 2, genderComb)
        self.table.setItem(0, 3, QTableWidgetItem("30"))
        self.table.setItem(0, 4, QTableWidgetItem("产品经理"))

        self.table.setItem(1, 0, QTableWidgetItem("005"))
        self.table.setItem(1, 1, QTableWidgetItem("Kitty"))
        genderComb = QComboBox()
        genderComb.addItem("男性")
        genderComb.addItem("女性")
        genderComb.setCurrentIndex(1)
        self.table.setCellWidget(1, 2, genderComb)
        self.table.setItem(1, 3, QTableWidgetItem("24"))
        self.table.setItem(1, 4, QTableWidgetItem("程序猿安慰师"))

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    table = TableSheet()
    table.show()
    sys.exit(app.exec_())