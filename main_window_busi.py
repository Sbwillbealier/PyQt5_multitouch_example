# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from mainWindowUI import Ui_mainWindow
from drawing_board_busi import DrawingBoardUIBusi
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, qApp, QDesktopWidget,
                             QMessageBox, QFileDialog, QAction, QSystemTrayIcon)
from PyQt5.QtCore import Qt, QEvent, QFile, QIODevice, QTextStream

import sys
from pykeyboard import PyKeyboard
import time


class MainWindowBusi(QMainWindow, Ui_mainWindow):
    def __init__(self):

        super(MainWindowBusi, self).__init__()
        self.setupUi(self)

        self.icon = QIcon("qrc\Icon.png")  # 窗体图标
        self.setWindowIcon(self.icon)

        # 设置控制窗体的位置
        cp = QDesktopWidget().availableGeometry()
        self.move(cp.width() - self.width() - 5, 0)

        # 设置退出按钮
        self.pushButton_exit.clicked.connect(self.closeAction)

        # 设置主窗口禁止调整大小
        self.setFixedSize(self.width(), self.height())

        # 设置窗体无边框
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint )
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint)

        # 获得白板对象
        self.dbb = DrawingBoardUIBusi()

        # 设置样式
        self.setStyle()

        # 窗体收起

        # 允许拖拽PPT文件到程序上
        self.setAcceptDrops(True)

        # 设置系统托盘
        self.addSystemTray()  # 设置系统托盘

    def addSystemTray(self):
        '''
        系统托盘，显示、隐藏主窗体，退出程序
        :return:
        '''
        minimizeAction = QAction("隐藏", self, triggered=self.hide)  # 隐藏菜单
        maximizeAction = QAction("显示", self, triggered=self.show)  # 显示菜单
        restoreAction = QAction("恢复", self, triggered=self.showNormal)  # 恢复菜单
        quitAction = QAction("退出", self, triggered=self.close)  # 退出菜单
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(minimizeAction)
        self.trayIconMenu.addAction(maximizeAction)
        self.trayIconMenu.addAction(restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.setWindowIcon(self.icon)
        self.trayIcon.setContextMenu(self.trayIconMenu)  # 添加右键菜单
        self.trayIcon.activated.connect(self.trayClick)  # 左键点击托盘

        self.trayIcon.show()

    def trayClick(self, event):
        '''
        双击系统托盘显示主窗体
        :param event:
        :return:
        '''
        if event == QSystemTrayIcon.DoubleClick:  # 双击
            self.showNormal()
        else:
            pass

    def mouseDoubleClickEvent(self, e):
        '''双击打开白板'''

        self.dbb.showMaximized()

    def mousePressEvent(self, event):
        '''鼠标点击事件--实现无边框窗体移动'''

        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        '''鼠标左键移动事件--实现无边框窗体移动'''

        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def keyPressEvent(self, event):
        '''键盘事件处理'''
        pass

    def contextMenuEvent(self, event):
        '''右键菜单'''

        cmenu = QMenu(self)

        showHideAct = cmenu.addAction('显示或隐藏', self.showHide)
        showQRcodeAct = cmenu.addAction('显示二维码', self.showQR)
        cmenu.addSeparator()

        openPPTAct = cmenu.addAction('打开PPT', self.openPPT)
        cmenu.addSeparator()

        settingsAct = cmenu.addAction('设置', self.settings)
        helpAct = cmenu.addAction('帮助', self.help)
        aboutAct = cmenu.addAction('关于', self.abuot)
        cmenu.addSeparator()

        exitAct = cmenu.addAction('退出', self.closeAction)

        cmenu.exec_(self.mapToGlobal(event.pos()))

    def closeAction(self):
        '''退出程序'''

        message = QMessageBox()
        message.setGeometry(200, 200, 200, 200)
        message.resize(200, 300)
        reply = message.question(self, 'Message',
                                 "确定退出?", QMessageBox.Yes |
                                 QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()
        if reply == QMessageBox.No:
            pass

    def showHide(self):
        '''显示或隐藏POT'''

        self.hide()

    def openPPT(self):
        '''打开PPT'''

        fileName = QFileDialog.getOpenFileName(self, '打开PPT',
                                               '.',
                                               "*.ppt;*.pptx;*.pptm;*.ppsx;*.pps;*.potx;*.pot;*.potm;*.odp;All File(*)")
        if fileName[0] and fileName[0].endswith(('ppt', 'pptx')):
            import os
            os.system('start ' + fileName[0])
        else:
            QMessageBox.information(self, '提示', '不是幻灯片文件，请重新选择！', QMessageBox.Yes)

        # 打开ppt
        k = PyKeyboard()
        time.sleep(4)
        k.tap_key(k.function_keys[5])
        time.sleep(3)

    def showQR(self):
        '''显示会议二维码或编号'''
        pass

    def settings(self):
        '''设置，打开设置界面'''
        pass

    def help(self):
        '''帮助功能'''
        pass

    def abuot(self):
        '''关于本软件'''
        pass

    def setStyle(self):
        '''加载样式表'''

        file = QFile('qrc\style3.qss')
        file.open(QIODevice.ReadOnly)
        styleSheet = QTextStream(file).readAll()
        qApp.setStyleSheet(styleSheet)

    def dragEnterEvent(self, e):
        '''拖拽输入事件'''

        if e.mimeData().hasUrls():
            if e.mimeData().urls()[0].fileName().split('.')[1] in ['ppt', 'pptx']:
                e.accept()
            else:
                QMessageBox.information(self, '提示', '不是幻灯片文件，请重新选择！', QMessageBox.Yes)
        else:
            e.ignore()

    def dropEvent(self, e):
        '''拖放处理'''

        from os import system
        url = e.mimeData().urls()[0].url()[8:]
        system('start ' + url)

        # 打开ppt
        k = PyKeyboard()
        time.sleep(4)
        k.tap_key(k.function_keys[5])
        time.sleep(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mW = MainWindowBusi()
    mW.show()
    sys.exit(app.exec_())
