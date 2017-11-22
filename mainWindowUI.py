# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(321, 146)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线 Light")
        mainWindow.setFont(font)
        mainWindow.setWindowOpacity(0.8)
        mainWindow.setToolTip("")
        mainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_share = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_share.setGeometry(QtCore.QRect(30, 30, 71, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_share.setFont(font)
        self.pushButton_share.setToolTip("")
        self.pushButton_share.setObjectName("pushButton_share")
        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(220, 30, 71, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setToolTip("")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.labelshow = QtWidgets.QLabel(self.centralwidget)
        self.labelshow.setGeometry(QtCore.QRect(110, 40, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelshow.setFont(font)
        self.labelshow.setText("")
        self.labelshow.setObjectName("labelshow")
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "白板"))
        self.pushButton_share.setText(_translate("mainWindow", "分享"))
        self.pushButton_exit.setText(_translate("mainWindow", "退出"))

