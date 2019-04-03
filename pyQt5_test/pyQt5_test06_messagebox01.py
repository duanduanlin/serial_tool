#!/user/bin/python3
# -*- coding:utf-8 -*-
'''
Creat a simple messagebox static version
'''
__author__ = 'Duanlin D'

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QGridLayout, QLabel, QPushButton, QFrame

class MessageBox(QWidget):
    def __init__(self):
        super(MessageBox, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("MessageBox")
        self.setGeometry(400, 400, 300, 290)

        self.questionLabel = QLabel("Question:")
        self.questionLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.infoLabel = QLabel("Information:")
        self.infoLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.warningLabel = QLabel("Warning:")
        self.warningLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.criticalLabel = QLabel("Critical:")
        self.criticalLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.aboutLabel = QLabel("About:")
        self.aboutLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.aboutQtLabel = QLabel("About QT:")
        self.aboutQtLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.resultLabel = QLabel("Result:")
        self.resultLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        questButton = QPushButton("...")
        questButton.clicked.connect(self.selectQuestion)
        infoButton = QPushButton("...")
        infoButton.clicked.connect(self.selectInfo)
        warningButton = QPushButton("...")
        warningButton.clicked.connect(self.selectWarning)
        criticalButton = QPushButton("...")
        criticalButton.clicked.connect(self.selectCritical)
        aboutButton = QPushButton("...")
        aboutButton.clicked.connect(self.selectAbout)
        aboutQtButton = QPushButton("...")
        aboutQtButton.clicked.connect(self.selectAboutQt)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.questionLabel, 0, 0)
        mainLayout.addWidget(questButton, 0, 1)
        mainLayout.addWidget(self.infoLabel, 1, 0)
        mainLayout.addWidget(infoButton, 1, 1)
        mainLayout.addWidget(self.warningLabel, 2, 0)
        mainLayout.addWidget(warningButton, 2, 1)
        mainLayout.addWidget(self.criticalLabel, 3, 0)
        mainLayout.addWidget(criticalButton, 3, 1)
        mainLayout.addWidget(self.aboutLabel, 4, 0)
        mainLayout.addWidget(aboutButton, 4, 1)
        mainLayout.addWidget(self.aboutQtLabel, 5, 0)
        mainLayout.addWidget(aboutQtButton, 5, 1)
        mainLayout.addWidget(self.resultLabel, 6, 1)

        self.setLayout(mainLayout)

    def selectQuestion(self):
        button = QMessageBox.question(self, "Question", "检测到程序有更新，是否安装最新版本？", QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)

        if button == QMessageBox.Ok:
            self.resultLabel.setText("<h2>Question:<font color=red>  OK</font></h2>")
        elif button == QMessageBox.Cancel:
            self.resultLabel.setText("<h2>Question:<font color=red>  Cancel</font></h2>")
        else:
            return

    def selectInfo(self):
        QMessageBox.information(self, "Information", "程序当前版本为V3.11")
        self.resultLabel.setText("Information")

    def selectWarning(self):
        button = QMessageBox.warning(self, "Warning", "恢复出厂设置将导致用户数据丢失，是否继续操作？",
                                     QMessageBox.Reset | QMessageBox.Help | QMessageBox.Cancel, QMessageBox.Reset)

        if button == QMessageBox.Reset:
            self.resultLabel.setText("<h2>Warning:<font color=red>  Reset</font></h2>")
        elif button == QMessageBox.Help:
            self.resultLabel.setText("<h2>Warning:<font color=red>  Help</font></h2>")
        elif button == QMessageBox.Cancel:
            self.resultLabel.setText("<h2>Warning:<font color=red>  Cancel</font></h2>")
        else:
            return

    def selectCritical(self):
        QMessageBox.critical(self, "Critical", "服务器宕机！")
        self.resultLabel.setText("<h2><font color=red>Critical</font></h2>")

    def selectAbout(self):
        QMessageBox.about(self, "About", "Copyright 2015 Tony zhu.\n All Right reserved.")
        self.resultLabel.setText("About")

    def selectAboutQt(self):
        QMessageBox.aboutQt(self, "About Qt")
        self.resultLabel.setText("About Qt")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myshow = MessageBox()
    myshow.show()
    sys.exit(app.exec_())
