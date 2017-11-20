# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drawingBoardUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_drawingBoard(object):
    def setupUi(self, drawingBoard):
        drawingBoard.setObjectName("drawingBoard")
        drawingBoard.resize(816, 602)
        drawingBoard.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        drawingBoard.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(drawingBoard)
        self.centralwidget.setObjectName("centralwidget")
        drawingBoard.setCentralWidget(self.centralwidget)

        self.retranslateUi(drawingBoard)
        QtCore.QMetaObject.connectSlotsByName(drawingBoard)

    def retranslateUi(self, drawingBoard):
        _translate = QtCore.QCoreApplication.translate
        drawingBoard.setWindowTitle(_translate("drawingBoard", "白板"))

