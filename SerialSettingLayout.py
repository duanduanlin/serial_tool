#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
串口工具设置面板
'''

__author__ = 'Duanlin D'

import sys
import os
import serial
import serial.tools.list_ports
import configparser

from PyQt5.QtWidgets import (QWidget, QApplication, QComboBox, QLabel, QPushButton, QHBoxLayout,
                             QVBoxLayout, QToolTip, QMessageBox)
from PyQt5.QtGui import (QIcon, QFont)


class SerialSettingLayout(QWidget):

    def __init__(self):
        super(SerialSettingLayout, self).__init__()

        self.serial = serial.Serial()

        self.open_close_button = QPushButton(u'打开串口')
        self.refresh_button = QPushButton(u'刷新串口')

        self.serial_setting_layout = QVBoxLayout()

        self.serial_parity_comboBox = QComboBox()
        self.serial_stopBits_comboBox = QComboBox()
        self.serial_data_comboBox = QComboBox()
        self.serial_baudRate_comboBox = QComboBox()
        self.serial_COM_comboBox = QComboBox()

        self.cfg_serial_dic = {}
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.cfg_path = ''
        self.cfg_dir = 'settings'
        self.conf_file_name = "cfg.ini"
        self.confParse = configparser.ConfigParser()
        self.is_serial_open = False

        self.serial_open_callback = self.serial_open_callback_fun
        self.serial_close_callback = self.serial_close_callback_fun
        self.init_ui()

    def init_ui(self):
        self.read_config()
        self.init_setting_layout()

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

    def init_setting_layout(self):
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

        self.serial_setting_layout.addLayout(serial_com_layout)
        self.serial_setting_layout.addLayout(serial_baud_rate_layout)
        self.serial_setting_layout.addLayout(serial_data_layout)
        self.serial_setting_layout.addLayout(serial_stop_bits_layout)
        self.serial_setting_layout.addLayout(serial_parity_layout)
        self.serial_setting_layout.addLayout(button_layout)

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

    def get_serial_setting(self):
        self.serial.port = self.serial_COM_comboBox.currentText()
        self.serial.baudrate = int(self.serial_baudRate_comboBox.currentText())
        self.serial.bytesize = int(self.serial_data_comboBox.currentText())
        self.serial.stopbits = int(self.serial_stopBits_comboBox.currentText())
        self.serial.parity = self.serial_parity_comboBox.currentText()
        self.serial.timeout = 0

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
            self.serial_open_callback()

    def close_serial(self):
        """
            关闭串口
            :return:
        """

        self.is_serial_open = False
        self.open_close_button.setText(u'打开串口')
        self.enable_serial_setting(True)
        self.serial_close_callback()
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

    def serial_open_callback_fun(self):
        pass

    def serial_close_callback_fun(self):
        pass

    def set_serial_open_callback(self, callback):
        if callable(callback):
            self.serial_open_callback = callback

    def set_serial_close_callback(self, callback):
        if callable(callback):
            self.serial_close_callback = callback

    def get_serial_setting_layout(self):
        """
        获取串口设置面板
        :return QVBoxLayout:
        """
        return self.serial_setting_layout

    def serial_readline(self):
        """
        读取一行,串口已打开则返回读取的内容，否则返回空字符串
        :return str:
        """
        if self.is_serial_open:
            try:
                text_line = self.serial.readline()
            except Exception as e:
                print(e)
                self.close_serial()
            else:
                return text_line.decode("utf-8", "ignore")
        else:
            return ""

    def serial_write(self, data):
        """
        串口发送字符串
        :param data 待发送的字符串str:
        :return:
        """
        if self.is_serial_open:
            try:
                self.serial.write(data.encode("utf-8", "ignore"))
            except Exception as e:
                print(e)

    def set_frame(self):
        """
        设置窗口布局
        :return:
        """
        self.setLayout(self.serial_setting_layout)

        self.setWindowTitle('serial qt tool')

        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(600, 400)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialSettingLayout()
    w.set_frame()
    sys.exit(app.exec_())
