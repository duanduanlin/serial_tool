#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat qt test program
'''

__author__ = 'Duanlin D'

import sys
import threading
import SerialSettingLayout as SSLayout

from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QGridLayout,
                             QVBoxLayout, QGroupBox, QToolTip, QDesktopWidget, QTextBrowser)
from PyQt5.QtGui import (QIcon, QFont, QColor)
from PyQt5.QtCore import (QBasicTimer)


class SerialQtTool(QWidget):
    Qt_Test_interval = 0.2
    Qt_Test_Count = 5
    Qt_Test_Message = "test_cmd"

    def __init__(self):
        super(SerialQtTool, self).__init__()
        self.read_data_timer = QBasicTimer()

        self.qt_test_count = SerialQtTool.Qt_Test_Count
        self.qt_test_interval = SerialQtTool.Qt_Test_interval
        self.is_qt_test_ok = False

        self.qt_test_button = QPushButton(u'start')
        self.log_view_groupBox = QGroupBox("log view")

        self.log_view_textBrowser = QTextBrowser()
        self.log_view_textBrowser.setFont(QFont('Helvetica', 28))

        self.serial_setting_groupBox = QGroupBox("serial_setting")
        self.serial_setting_layout = SSLayout.SerialSettingLayout()
        self.serial_setting_layout.set_serial_open_callback(self.start_read_data())
        self.serial_setting_layout.set_serial_close_callback(self.stop_read_data())

        self.init_ui()

    def init_log_view_group(self):
        """
        初始化打印窗口
        :return:
        """

        log_view_layout = QVBoxLayout()
        log_view_layout.addWidget(self.log_view_textBrowser)

        self.log_view_groupBox.setLayout(log_view_layout)

    def init_serial_setting_group(self):

        QToolTip.setFont(QFont('SansSerif', 10))
        self.qt_test_button.setToolTip("start qt test")
        self.qt_test_button.clicked.connect(self.qt_test_button_handle)
        self.qt_test_button.setEnabled(False)

        serial_setting_layout = self.serial_setting_layout.get_serial_setting_layout()
        serial_setting_layout.addWidget(self.qt_test_button)

        self.serial_setting_groupBox.setLayout(serial_setting_layout)

    def init_ui(self):
        """
        初始化界面布局
        :return:
        """

        self.init_serial_setting_group()
        self.init_log_view_group()
        self.set_frame()

    def qt_test_fun(self):
        """
        产测执行程序，以一定的时间间隔执行指定次数，直到成功为止
        :return:
        """
        self.serial_setting_layout.serial_write(SerialQtTool.Qt_Test_Message)
        self.qt_test_count -= 1
        if self.qt_test_count > 0:
            self.qt_fun_timer = threading.Timer(self.qt_test_interval, self.qt_test_fun)
            self.qt_fun_timer.start()

    def qt_test_button_handle(self):
        """
        产测按钮响应程序
        :return:
        """
        if self.serial_setting_layout.is_serial_open:
            self.qt_test_button.setEnabled(False)
            self.log_view_textBrowser.clear()
            self.qt_test_count = SerialQtTool.Qt_Test_Count
            self.qt_fun_timer = threading.Timer(self.qt_test_interval, self.qt_test_fun)
            self.qt_fun_timer.start()

    def timerEvent(self, e):
        text_line = self.serial_setting_layout.serial_readline()

        if text_line and "ok" in text_line:
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
        self.qt_test_button.setEnabled(True)
        pass

    def stop_read_data(self):
        """
        停止读取数据
        :return:
        """
        self.read_data_timer.stop()
        self.qt_test_button.setEnabled(False)
        pass

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
