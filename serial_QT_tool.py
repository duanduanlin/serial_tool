#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat qt test program
'''
import time

import serial

__author__ = 'Duanlin D'

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QComboBox, QLabel, QPushButton, QHBoxLayout, QGridLayout,
                             QVBoxLayout, QGroupBox, QToolTip, QDesktopWidget, QMessageBox, QTextBrowser)
from PyQt5.QtGui import (QIcon, QFont, QColor)
from PyQt5.QtCore import (QBasicTimer)
import serial.tools.list_ports
import configparser
import os
import threading


class SerialQtTool(QWidget):
    Qt_Test_interval = 0.2
    Qt_Test_Count = 5

    def __init__(self):
        super(SerialQtTool, self).__init__()

        self.qt_test_count = SerialQtTool.Qt_Test_Count
        self.qt_test_interval = SerialQtTool.Qt_Test_interval
        self.is_qt_test_ok = False
        self.serial = serial.Serial()
        self.read_data_timer = QBasicTimer()

        self.open_close_button = QPushButton(u'打开串口')
        self.refresh_button = QPushButton(u'刷新串口')
        self.qt_test_button = QPushButton(u'start')
        self.serial_setting_groupBox = QGroupBox("serial setting")
        self.log_view_groupBox = QGroupBox("log view")

        self.serial_parity_comboBox = QComboBox()
        self.serial_stopBits_comboBox = QComboBox()
        self.serial_data_comboBox = QComboBox()
        self.serial_baudRate_comboBox = QComboBox()
        self.serial_COM_comboBox = QComboBox()

        self.log_view_textBrowser = QTextBrowser()
        self.log_view_textBrowser.setFont(QFont('Helvetica', 28))
        self.is_serial_open = False

        self.cfg_serial_dic = {}
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.cfg_path = ''
        self.cfg_dir = 'settings'
        self.conf_file_name = "cfg.ini"
        self.confParse = configparser.ConfigParser()

        self.init_ui()

    @staticmethod
    def get_port_list():
        """
        获取当前系统所有COM口
        :return:
        """
        com_list = []
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            com_list.append(port[0])
        return com_list

    def init_logView_group(self):
        """
        初始化打印窗口
        :return:
        """

        log_view_layout = QVBoxLayout()
        log_view_layout.addWidget(self.log_view_textBrowser)

        self.log_view_groupBox.setLayout(log_view_layout)

    def init_setting_group(self):
        """
        初始化串口设置组
        :return:
        """

        serial_com_label = QLabel(u'串口号')
        self.serial_COM_comboBox.addItems(self.get_port_list())
        self.serial_COM_comboBox.setCurrentText(self.cfg_serial_dic.get('com', 'COM1'))

        serial_baud_rate_label = QLabel(u'波特率')
        self.serial_baudRate_comboBox.addItems(['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                                                '38400', '56000', '57600', '115200', '128000', '256000'])
        self.serial_baudRate_comboBox.setCurrentText(self.cfg_serial_dic.get('baudrate', '9600'))

        serial_data_label = QLabel(u'数据位')
        self.serial_data_comboBox.addItems(['5', '6', '7', '8'])
        self.serial_data_comboBox.setCurrentText(self.cfg_serial_dic.get('data', '8'))

        serial_stop_bits_label = QLabel(u'停止位')
        self.serial_stopBits_comboBox.addItems(['1', '1.5', '2'])
        self.serial_stopBits_comboBox.setCurrentText(self.cfg_serial_dic.get('stopbits', '1'))

        serial_parity_label = QLabel(u'奇偶校验位')
        self.serial_parity_comboBox.addItems(['N', 'E', 'O', 'M', 'S'])
        self.serial_parity_comboBox.setCurrentText(self.cfg_serial_dic.get('parity', 'N'))

        QToolTip.setFont(QFont('SansSerif', 10))
        self.open_close_button.setToolTip("open or close selected port")
        self.refresh_button.setToolTip("refresh current port")
        self.open_close_button.clicked.connect(self.open_close_button_handle)
        self.refresh_button.clicked.connect(self.refresh_button_handle)
        self.qt_test_button.clicked.connect(self.start_qt_test)
        self.qt_test_button.setEnabled(False)

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

        button_qt_layout = QHBoxLayout()
        button_qt_layout.addWidget(self.qt_test_button)

        serial_setting_layout = QVBoxLayout()

        serial_setting_layout.addLayout(serial_com_layout)
        serial_setting_layout.addLayout(serial_baud_rate_layout)
        serial_setting_layout.addLayout(serial_data_layout)
        serial_setting_layout.addLayout(serial_stop_bits_layout)
        serial_setting_layout.addLayout(serial_parity_layout)
        serial_setting_layout.addLayout(button_layout)
        serial_setting_layout.addLayout(button_qt_layout)
        # erial_setting_layout.addStretch()
        self.serial_setting_groupBox.setLayout(serial_setting_layout)

    def init_ui(self):
        """
        初始化界面布局
        :return:
        """
        self.read_config()
        self.init_setting_group()
        self.init_logView_group()
        self.set_frame()

    def qt_test_fun(self):
        data = "test_cmd"
        try:
            self.serial.write(data.encode("utf-8", "ignore"))
        except:
            print("error")
            pass
        self.qt_test_count -= 1
        if self.qt_test_count > 0:
            self.qt_fun_timer = threading.Timer(self.qt_test_interval, self.qt_test_fun)
            self.qt_fun_timer.start()



    def start_qt_test(self):
        if self.serial.is_open:
            self.qt_test_button.setEnabled(False)
            self.log_view_textBrowser.clear()
            self.qt_test_count = SerialQtTool.Qt_Test_Count
            self.qt_fun_timer = threading.Timer(self.qt_test_interval, self.qt_test_fun)
            self.qt_fun_timer.start()


    def read_config(self):
        """
        读取串口配置
        :return:
        """
        self.cfg_path = os.path.join(self.current_path, self.cfg_dir, self.conf_file_name)
        if self.confParse.read(self.cfg_path, encoding='utf-8'):
            # sections = self.confParse.sections()
            #  print(sections)
            try:
                items = self.confParse.items('serial_setting')
                self.cfg_serial_dic = dict(items)
                # print(self.cfg_serial_dic)
            except configparser.NoSectionError:
                self.confParse.add_section('serial_setting')
                self.confParse.write(open(self.cfg_path, 'w'))
        else:
            if not os.path.exists(os.path.join(self.current_path, self.cfg_dir)):
                os.mkdir(os.path.join(self.current_path, self.cfg_dir))

            self.confParse.add_section('serial_setting')
            self.confParse.write(open(self.cfg_path, 'w'))

    def timerEvent(self, e):
        if self.serial.is_open:
            try:
                text_line = self.serial.readline()
            except:
                self.close_serial()
            else:
                if text_line and "ok" in text_line.decode("utf-8", "ignore"):
                    self.log_view_textBrowser.setTextColor(QColor(0, 255, 0))
                    self.log_view_textBrowser.setText("测试成功")
                    self.qt_fun_timer.cancel()
                    self.qt_test_button.setEnabled(True)
                elif self.qt_test_count <= 0:
                    self.log_view_textBrowser.setTextColor(QColor(255, 0, 0))
                    self.log_view_textBrowser.setText("测试失败")
                    self.qt_test_button.setEnabled(True)

    def start_read_data(self):
        """
        开始读取数据
        :return:
        """
        self.read_data_timer.start(2, self)
        pass

    def stop_read_data(self):
        """
        停止读取数据
        :return:
        """
        self.read_data_timer.stop()
        pass

    def get_serial_setting(self):
        self.serial.port = self.serial_COM_comboBox.currentText()
        self.serial.baudrate = int(self.serial_baudRate_comboBox.currentText())
        self.serial.bytesize = int(self.serial_data_comboBox.currentText())
        self.serial.stopbits = int(self.serial_stopBits_comboBox.currentText())
        self.serial.parity = self.serial_parity_comboBox.currentText()
        self.serial.timeout = 0

    def save_config(self):
        """
        保存配置
        :return:
        """
        self.confParse.set('serial_setting', 'com', self.serial.port)
        self.confParse.set('serial_setting', 'baudRate', str(self.serial.baudrate))
        self.confParse.set('serial_setting', 'data', str(self.serial.bytesize))
        self.confParse.set('serial_setting', 'stopBits', str(self.serial.stopbits))
        self.confParse.set('serial_setting', 'parity', self.serial.parity)
        self.confParse.write(open(self.cfg_path, 'w'))

    def open_serial(self):
        """
            打开串口
            :return:
        """
        self.get_serial_setting()
        self.save_config()

        try:
            self.serial.open()
        except serial.SerialException:
            QMessageBox.critical(self, "Critical", "无法打开串口！！")
        else:
            self.is_serial_open = True
            self.open_close_button.setText(u'关闭串口')
            self.enable_serial_setting(False)
            self.qt_test_button.setEnabled(True)
            self.start_read_data()

    def close_serial(self):
        """
            关闭串口
            :return:
        """

        self.is_serial_open = False
        self.open_close_button.setText(u'打开串口')
        self.enable_serial_setting(True)
        self.qt_test_button.setEnabled(False)
        self.stop_read_data()
        self.serial.close()

    def open_close_button_handle(self):
        """
        处理打开或关闭串口按键事件
        :return:
        """
        if self.is_serial_open:
            self.close_serial()
        else:
            self.open_serial()

    def refresh_button_handle(self):
        self.serial_COM_comboBox.clear()
        self.serial_COM_comboBox.addItems(self.get_port_list())

    def enable_serial_setting(self, enable):
        """
        使能串口设置组件和刷新串口组件
        :param enable: bool ,True: enable,False: disable
        :return:
        """
        self.refresh_button.setEnabled(enable)
        self.serial_parity_comboBox.setEnabled(enable)
        self.serial_stopBits_comboBox.setEnabled(enable)
        self.serial_data_comboBox.setEnabled(enable)
        self.serial_baudRate_comboBox.setEnabled(enable)
        self.serial_COM_comboBox.setEnabled(enable)


    def center(self):
        """
        将程序串口置于屏幕中央
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_frame(self):
        """
        设置窗口布局
        :return:
        """
        main_layout = QGridLayout()
        main_layout.addWidget(self.log_view_groupBox, 0, 0, 1, 4)
        main_layout.addWidget(self.serial_setting_groupBox, 0, 5)
        self.setLayout(main_layout)

        self.setWindowTitle('serial qt tool')

        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(600, 400)
        self.center()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialQtTool()
    sys.exit(app.exec_())
