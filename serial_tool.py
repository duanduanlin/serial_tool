#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat a simple window
'''
import serial

__author__ = 'Duanlin D'

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QComboBox, QLabel, QPushButton, QHBoxLayout, QGridLayout,
    QVBoxLayout, QGroupBox, QToolTip, QDesktopWidget, QMessageBox, QTextEdit, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
import serial.tools.list_ports


class SerialTool(QWidget):

    def __init__(self):
        super(SerialTool, self).__init__()
        self.open_close_button = QPushButton(u'打开串口')
        self.refresh_button = QPushButton(u'刷新串口')
        self.serial_setting_groupBox = QGroupBox("serial setting")
        self.log_view_groupBox = QGroupBox("log view")

        self.serial_parity_comboBox = QComboBox()
        self.serial_stopBits_comboBox = QComboBox()
        self.serial_data_comboBox = QComboBox()
        self.serial_baudRate_comboBox = QComboBox()
        self.serial_COM_comboBox = QComboBox()

        self.log_view_textEdit = QTextEdit()
        self.is_open = False
        self.init_ui()

    def init_ui(self):
        self.init_setting_group()
        self.init_logView_group()
        self.set_frame()

    def init_setting_group(self):
        """
        初始化串口设置组
        :return:
        """

        serial_com_label = QLabel(u'串口号')
        self.serial_COM_comboBox.addItems(self.get_port_list())

        serial_baud_rate_label = QLabel(u'波特率')
        self.serial_baudRate_comboBox.addItems(['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                                                '38400', '56000', '57600', '115200', '128000', '256000'])
        self.serial_baudRate_comboBox.setCurrentIndex(6)

        serial_data_label = QLabel(u'数据位')
        self.serial_data_comboBox.addItems(['5', '6', '7', '8'])
        self.serial_data_comboBox.setCurrentIndex(3)

        serial_stop_bits_label = QLabel(u'停止位')
        self.serial_stopBits_comboBox.addItems(['1', '1.5', '2'])
        self.serial_stopBits_comboBox.setCurrentIndex(0)

        serial_parity_label = QLabel(u'奇偶校验位')
        self.serial_parity_comboBox.addItems(['NONE', 'EVEN', 'ODD', 'MARK', 'SPACE'])
        self.serial_parity_comboBox.setCurrentIndex(0)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.open_close_button.setToolTip("open or close selected port")
        self.refresh_button.setToolTip("refresh current port")
        self.open_close_button.clicked.connect(self.open_close)
        self.refresh_button.clicked.connect(self.refresh)

        serial_com_layout = QHBoxLayout()
        serial_com_layout.addWidget(serial_com_label)
        serial_com_layout.addWidget(self.serial_COM_comboBox)

        serial_baud_rate_layout = QHBoxLayout()
        serial_baud_rate_layout.addWidget(serial_baud_rate_label)
        serial_baud_rate_layout.addWidget(self.serial_baudRate_comboBox)

        serial_data_layout = QHBoxLayout()
        serial_data_layout.addWidget(serial_data_label)
        serial_data_layout.addWidget(self.serial_data_comboBox)

        serial_stop_bits_layout = QHBoxLayout()
        serial_stop_bits_layout.addWidget(serial_stop_bits_label)
        serial_stop_bits_layout.addWidget(self.serial_stopBits_comboBox)

        serial_parity_layout = QHBoxLayout()
        serial_parity_layout.addWidget(serial_parity_label)
        serial_parity_layout.addWidget(self.serial_parity_comboBox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_close_button)
        button_layout.addWidget(self.refresh_button)

        serial_setting_layout = QVBoxLayout()

        serial_setting_layout.addLayout(serial_com_layout)
        serial_setting_layout.addLayout(serial_baud_rate_layout)
        serial_setting_layout.addLayout(serial_data_layout)
        serial_setting_layout.addLayout(serial_stop_bits_layout)
        serial_setting_layout.addLayout(serial_parity_layout)
        serial_setting_layout.addLayout(button_layout)
        #erial_setting_layout.addStretch()
        self.serial_setting_groupBox.setLayout(serial_setting_layout)

    def init_logView_group(self):
        clear_screen_button = QPushButton("清空当前打印")
        view_log_button = QPushButton("查看日志")
        clear_screen_button.clicked.connect(self.clear_screen)
        view_log_button.clicked.connect(self.open_log_file)

        view_button_layout = QHBoxLayout()
        view_button_layout.addWidget(clear_screen_button)
        view_button_layout.addWidget(view_log_button)

        log_view_layout = QVBoxLayout()
        log_view_layout.addLayout(view_button_layout)
        log_view_layout.addWidget(self.log_view_textEdit)

        self.log_view_groupBox.setLayout(log_view_layout)

    def clear_screen(self):
        self.log_view_textEdit.clear()
        # create a new log file
        pass

    def open_log_file(self):
        current_file_path = QFileDialog().getExistingDirectory()
        QFileDialog.getOpenFileName(self, "Open log File", current_file_path, "Log files(*.log)")

    @staticmethod
    def get_port_list():
        com_list = []
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            com_list.append(port[0])
        return com_list

    def open_close(self):
        if self.is_open:
            self.is_open = False
            self.open_close_button.setText(u'打开串口')
        else:
            self.is_open = True
            self.open_close_button.setText(u'关闭串口')

    def refresh(self):
        button = QMessageBox.question(self, "Question", "确定刷新？", QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.serial_COM_comboBox.clear()
            self.serial_COM_comboBox.addItems(self.get_port_list())
        elif button == QMessageBox.Cancel:
            pass
        else:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_frame(self):
        main_layout = QGridLayout()
        main_layout.addWidget(self.log_view_groupBox, 0, 0, 2, 4)
        main_layout.addWidget(self.serial_setting_groupBox, 0, 5)
        self.setLayout(main_layout)

        self.setWindowTitle('serial tool')
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(1000, 600)
        self.center()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialTool()
    sys.exit(app.exec_())
