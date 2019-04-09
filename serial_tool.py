#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat a simple window
'''
import serial

__author__ = 'Duanlin D'

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QComboBox, QLabel, QPushButton, QHBoxLayout, QGridLayout, QVBoxLayout
import serial.tools.list_ports

class SerialTool(QWidget):
    def __init__(self):
        super(SerialTool, self).__init__()
        self.initUi()

    def initUi(self):
        self.is_open = False
        self.setWindowTitle('serial tool')
        self.setGeometry(300, 100, 800, 600)

        SerialCOMLabel = QLabel(u'串口号')
        self.SerialCOMComboBox = QComboBox()
        self.SerialCOMComboBox.addItems(self.Port_List())

        SerialBaudRateLabel = QLabel(u'波特率')
        self.SerialBaudRateComboBox = QComboBox()
        self.SerialBaudRateComboBox.addItems(['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                                              '38400', '56000', '57600', '115200','128000', '256000'])
        self.SerialBaudRateComboBox.setCurrentIndex(6)

        SerialDataLabel = QLabel(u'数据位')
        self.SerialDataComboBox = QComboBox()
        self.SerialDataComboBox.addItems(['5', '6', '7', '8'])
        self.SerialDataComboBox.setCurrentIndex(3)

        SerialSTOPBitsLabel = QLabel(u'停止位')
        self.SerialStopBitsComboBox = QComboBox()
        self.SerialStopBitsComboBox.addItems(['1', '1.5', '2'])
        self.SerialStopBitsComboBox.setCurrentIndex(0)

        SerialParityLabel = QLabel(u'奇偶校验位')
        self.SerialParityComboBox = QComboBox()
        self.SerialParityComboBox.addItems(['NONE', 'EVEN', 'ODD', 'MARK', 'SPACE'])
        self.SerialParityComboBox.setCurrentIndex(0)

        self.OpenCloseButton = QPushButton(u'打开串口')
        self.ReFreshButton = QPushButton(u'刷新串口')
        self.OpenCloseButton.clicked.connect(self.open_close)
        self.OpenCloseButton.clicked.connect(self.refresh)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.OpenCloseButton)
        buttonLayout.addWidget(self.ReFreshButton)
        buttonLayout.addStretch()

        layout = QGridLayout()
        layout.addWidget(SerialCOMLabel, 0, 0)
        layout.addWidget(self.SerialCOMComboBox, 0, 1)
        layout.addWidget(SerialBaudRateLabel, 1, 0)
        layout.addWidget(self.SerialBaudRateComboBox, 1, 1)
        layout.addWidget(SerialDataLabel, 2, 0)
        layout.addWidget(self.SerialDataComboBox, 2, 1)
        layout.addWidget(SerialSTOPBitsLabel, 3, 0)
        layout.addWidget(self.SerialStopBitsComboBox, 3, 1)
        layout.addWidget(SerialParityLabel, 4, 0)
        layout.addWidget(self.SerialParityComboBox, 4, 1)

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(layout)
        mainlayout.addLayout(buttonLayout)
        self.setLayout(mainlayout)

    def Port_List(self):
        Com_List = []
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            Com_List.append(port[0])
        return Com_List

    def open_close(self):
        if self.is_open:
            self.is_open = False
            self.OpenCloseButton.setText(u'打开串口')
        else:
            self.is_open = True
            self.OpenCloseButton.setText(u'关闭串口')

    def refresh(self):
        self.SerialCOMComboBox.clear()
        self.SerialCOMComboBox.addItems(self.Port_List())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialTool()
    w.show()
    sys.exit(app.exec_())
