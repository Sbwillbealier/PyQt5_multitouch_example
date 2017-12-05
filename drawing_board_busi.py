# -*- coding: utf-8 -*-

import sys
import logging
import os

from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon, QBrush, QPixmapCache
from PyQt5.QtCore import Qt, QDateTime, QPoint
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget,
                             QPushButton, QMenu, QFileDialog)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class DrawingBoardUIBusi(QMainWindow):

    def __init__(self):
        super(DrawingBoardUIBusi, self).__init__()

        self.init_parameters()  # 初始化系统参数
        self.setupUi()          # 创建UI

    def setupUi(self):
        '''
        创建UI,
        :return:
        '''

        self.setObjectName('drawWindow')    # 对象名
        self.setWindowTitle('白板')  # 设置标题
        self.resize(self.resolution.width(), self.resolution.height())
        self.setWindowIcon(QIcon("qrc\Icon.png"))  # 设置图标
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint)  # 任务栏隐藏图标
        self.setWindowTitle('当前' + str(self.page) + '页')    # 标题显示第几页
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())        # 设置主窗口禁止调整大小

        # 创建白板的功能键
        btn_names = ['清屏', '保存', '切换', '上一页', '下一页', '黑笔', '蓝笔', '红笔', '擦除', '功能', '恢复', '加载']

        # 各个按钮的位置
        positions = [(self.resolution.width() - self.resolution.height() / len(btn_names),
                      (y * self.resolution.height() / len(btn_names))) for y in range(0, len(btn_names))]

        # 每个功能按钮的高度
        height = (self.resolution.height() / len(btn_names)) * 0.98

        '''要重构这部分代码'''
        # 清屏
        self.btn_clean = QPushButton(btn_names[0], self)
        self.btn_clean.resize(height, height)
        self.btn_clean.move(positions[0][0], positions[0][1])
        self.btn_clean.clicked.connect(self.clearScree)

        # 保存
        self.btn_savePicture = QPushButton(btn_names[1], self)
        self.btn_savePicture.resize(height, height)
        self.btn_savePicture.move(positions[1][0], positions[1][1])
        self.btn_savePicture.clicked.connect(lambda: self.savePicture(False))

        # 切换
        self.btn_switch = QPushButton(btn_names[2], self)
        self.btn_switch.resize(height, height)
        self.btn_switch.move(positions[2][0], positions[2][1])
        self.btn_switch.clicked.connect(self.switch)

        # 上一页
        self.btn_previousPage = QPushButton(btn_names[3], self)
        self.btn_previousPage.resize(height, height)
        self.btn_previousPage.move(positions[3][0], positions[3][1])
        self.btn_previousPage.clicked.connect(self.previousPage)

        # 下一页
        self.btn_nextPage = QPushButton(btn_names[4], self)
        self.btn_nextPage.resize(height, height)
        self.btn_nextPage.move(positions[4][0], positions[4][1])
        self.btn_nextPage.clicked.connect(self.nextPage)

        # 黑笔
        self.btn_changeColor1 = QPushButton(btn_names[5], self)
        self.btn_changeColor1.resize(height, height)
        self.btn_changeColor1.move(positions[5][0], positions[5][1])
        self.btn_changeColor1.clicked.connect(lambda: self.changeColor(0))
        self.btn_changeColor1.setEnabled(True)

        # 蓝笔
        self.btn_changeColor2 = QPushButton(btn_names[6], self)
        self.btn_changeColor2.resize(height, height)
        self.btn_changeColor2.move(positions[6][0], positions[6][1])
        self.btn_changeColor2.clicked.connect(lambda: self.changeColor(1))
        self.btn_changeColor2.setEnabled(True)

        # 红笔
        self.btn_changeColor3 = QPushButton(btn_names[7], self)
        self.btn_changeColor3.resize(height, height)
        self.btn_changeColor3.move(positions[7][0], positions[7][1])
        self.btn_changeColor3.clicked.connect(lambda: self.changeColor(2))
        self.btn_changeColor3.setEnabled(True)

        # 擦除
        self.btn_erase = QPushButton(btn_names[8], self)
        self.btn_erase.resize(height, height)
        self.btn_erase.move(positions[8][0], positions[8][1])
        self.btn_erase.clicked.connect(self.erase)

        # 功能
        self.btn_startSharing = QPushButton(btn_names[9], self)
        self.btn_startSharing.resize(height, height)
        self.btn_startSharing.move(positions[9][0], positions[9][1])
        self.btn_startSharing.clicked.connect(self.startSharing)

        # 恢复
        self.btn_restorePicture = QPushButton(btn_names[10], self)
        self.btn_restorePicture.resize(height, height)
        self.btn_restorePicture.move(positions[10][0], positions[10][1])
        self.btn_restorePicture.clicked.connect(self.restorePicture)

        # 加载
        self.btn_loadPicture = QPushButton(btn_names[11], self)
        self.btn_loadPicture.resize(height, height)
        self.btn_loadPicture.move(positions[11][0], positions[11][1])
        self.btn_loadPicture.clicked.connect(self.loadPicture)

    def init_parameters(self):
        '''
        初始化系统参数,可读取系统配置文件
        :return:
        '''

        self.resolution = QDesktopWidget().availableGeometry()  # 获取显示器的分辨率-->(0, 0, 1366, 728)
        self.monitor = QDesktopWidget()  # 获得显示器的物理尺寸
        # self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint)  # 任务栏隐藏图标

        # 会议号
        self.meetingID = 0 # 当前会议号
        # 页数记录
        self.page = 1  # 当前所在页页码
        self.pages = 1  # 总页数
        self.isWritting = False # 是否正在输入
        self.isWritten = False # 记录当前页是否有新写入

        # 记录笔迹（坐标，颜色）
        self.penColor = 0  # 笔的初始颜色黑色
        self.pos_xyc = []  # [((x, y), c)]  c->0 1 2 3
        self.pos_pages = {}  # 存放所有页笔画路径{page : pos_xyc}

        # 设置不追踪鼠标
        self.setMouseTracking(False)

        # 使用指定的画笔，宽度，钢笔样式，帽子样式和连接样式构造笔
        self.pen = QPen(Qt.black, 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        # 绘制在窗体上的painter
        # self.paintToWindow = QPainter(self)
        # self.paintToWindow.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # 画布pix
        self.pix = QPixmap(self.resolution.size())
        self.pix.fill(Qt.white)

        # 绘制在画布上的painter
        # self.paint_to_pix = QPainter(self.pix)
        # self.paint_to_pix.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # self.paint_to_pix.setPen(self.pen)

        # 黑板擦
        self.paintEase = QPainter(self)
        self.paintEase.setPen(QPen(Qt.black, Qt.DashLine))
        self.paintEase.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        # 是否擦除
        self.eraseable = False

        # 起点终点
        self.lastPoint = QPoint()
        self.endPoint = QPoint()


    def paintEvent(self, event):
        '''绘图事件'''

        # logger.debug('开始抒写')

        if self.isWritting:
            # 绘制在画布上

            paint_to_pix = QPainter(self.pix)
            paint_to_pix.setRenderHint(QPainter.SmoothPixmapTransform, True)
            paint_to_pix.setPen(self.pen)

            # 根据鼠标指针前后两个位置绘制直线
            paint_to_pix.drawLine(self.lastPoint, self.endPoint)

            # 让前一个坐标值等于后一个坐标值，
            self.lastPoint = self.endPoint

        # logger.debug('绘制在屏幕上')
        # 绘制在屏幕上
        painter_to_window = QPainter(self)
        painter_to_window.setPen(self.pen)
        painter_to_window.drawPixmap(0, 0, self.pix)

    def mousePressEvent(self, event):

        # 鼠标左键按下
        if event.button() == Qt.LeftButton:
            self.isWritten = True # 当前页有输入或改动
            self.isWritting = True # 已开始抒写
            self.lastPoint = event.pos()
            self.endPoint = self.lastPoint
            logger.debug('点击左键')

    def mouseMoveEvent(self, event):
        '''
            调用update()函数在这里相当于调用paintEvent()函数
        '''

        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos()
            # 进行重新绘制
            self.update()
            logger.debug('鼠标移动')

    def mouseReleaseEvent(self, event):

        # 鼠标左键释放
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            # 进行重新绘制
            self.update()
            self.isWritting = False # 已停止抒写
            logger.debug('左键释放')


    def keyPressEvent(self, event):
        '''
        键盘事件
        :param event:
        :return:
        '''

        # ESC最小化白板
        if event.key() == Qt.Key_Escape:
            self.hide()

    def contextMenuEvent(self, event):
        '''
        白板中的右键菜单
        :param event:
        :return:
        '''

        qmenu = QMenu(self)

        qmenu.addAction('清屏', self.clearScree)

        savePictureAct = qmenu.addAction('保存')
        savePictureAct.triggered.connect(lambda: self.savePicture(False))
        qmenu.addAction('切换', self.switch)

        qmenu.addSeparator()
        qmenu.addAction('上一页', self.previousPage)
        qmenu.addAction('下一页', self.nextPage)
        qmenu.addSeparator()

        self.changeColorBlack = qmenu.addAction('黑笔')
        self.changeColorBlack.triggered.connect(lambda: self.changeColor(0))
        self.changeColorBlue = qmenu.addAction('蓝笔')
        self.changeColorBlue.triggered.connect(lambda: self.changeColor(1))
        self.changeColorRed = qmenu.addAction('红笔')
        self.changeColorRed.triggered.connect(lambda: self.changeColor(2))
        qmenu.addAction('擦除', self.erase)
        qmenu.addSeparator()

        # self.changeThickness = qmenu.addAction('笔的粗细', self.changeThickness())
        # qmenu.addSeparator()

        qmenu.addAction('功能', self.startSharing)
        qmenu.addAction('恢复', self.restorePicture)
        qmenu.addAction('加载', self.loadPicture)

        self.action = qmenu.exec_(self.mapToGlobal(event.pos()))

    def loadPicture(self):
        '''加载本地图片'''

    def restorePicture(self):
        pass

    def startSharing(self):
        pass

    def changeThickness(self):
        pass

    def erase(self):

        if self.eraseable==False:
            self.eraseable = True
            self.pen.setColor(Qt.white) # 设置黑板擦的颜色为白色，与画板颜色一致
            self.pen.setWidth(18) # 设置黑板擦宽度
            # self.paint_to_pix.setPen(self.pen) # 更新paint_to_pix
            self.penColor = 3
        else:
            self.eraseable =False
            self.changeColor(0)

    def changeColor(self, colorNum):
        '''
        换颜色
        :param colorNum: 颜色号
        :return:
        '''

        # 关闭黑板擦
        self.eraseable = False

        # 笔的颜色
        colorDic = {0: Qt.black, 1: Qt.blue, 2: Qt.red}

        self.pen.setColor(colorDic[colorNum])
        # self.paint_to_pix.setPen(self.pen)  # 更新paint_to_pix
        self.penColor = colorNum
        self.pen.setWidth(4)

    def nextPage(self):
        '''
        切换下一页画布
        :return:
        '''

        if self.isWritten:
            # 当前页有输入或改动则保存当前页
            self.savePicture(True)
            # self.pos_pages[self.page] = self.pos_xyc  # 记录当前页笔画路径
            self.isWritten = False # 关闭改动标志

        if self.page == self.pages:

            # 开辟新一页，总页数加一
            # self.pos_xyc = []  # 当前页路径清空
            self.pages += 1  # 页总数加一
            self.pix.fill(Qt.white)  # 清空画布

        else:
            # 当前页并非最后一页
            fileName = str(self.page + 1)
            readFileName = os.path.join(self.filePath, 'temp', fileName + '.png')
            QPixmapCache.clear()
            self.pix.load(readFileName)

            # self.pos_xyc = self.pos_pages[self.page + 1]


        self.update()   # 更新内容
        self.page = self.page + 1  # 当前页码加一
        self.setWindowTitle('当前' + str(self.page) + '/' + str(self.pages) + '页')  # 更新标题栏显示的页码

        logger.debug('下翻页第%s页', self.page)

    def previousPage(self):
        '''
        切换到上一页画布
        :return:
        '''

        if self.isWritten or (self.page == self.pages):
            # 当前页有输入或改动则保存当前页
            self.savePicture(True)
            # self.pos_pages[self.page] = self.pos_xyc  # 记录当前页笔画路径
            self.isWritten = False # 关闭改动标志

        if self.page > 1:
            # 当前页码非第一页
            self.page -= 1 # 当前页码减一
            fileName = str(self.page)
            readFileName = os.path.join(self.filePath, 'temp', fileName + '.png')
            QPixmapCache.clear() # 清空画布
            self.pix.load(readFileName)

            # self.pos_xyc = self.pos_pages[self.page]

        else:
            # 当前页码为第一页
            pass

        self.update()  # 更新内容
        self.setWindowTitle('当前' + str(self.page) + '/' + str(self.pages) + '页')  # 更新标题栏显示的页码

        logger.debug('上翻页第%s页', self.page)

    def switch(self):
        '''切换'''

        self.showMinimized()

    def savePicture(self, flag=True, meetingID='201711'):
        '''
            将当前白板上的内容保存成图片
            flag = True,为自动保存
            flag = False为用户保存
        '''
        # 保存目录 './save/日期+会议号/'
        time = QDateTime.currentDateTime().toString("yyyy-MM-dd_")
        self.meetingID = meetingID
        self.filePath = os.path.join(os.getcwd(), 'save', time + self.meetingID)
        # 创建目录
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)
            os.makedirs(os.path.join(self.filePath, 'temp'))

        if flag:

            # 自动保存分为两部分：1.保存图片到本地 2.保存保存路径json文件到本地
            # 1.保存图片到本地
            # fileName = QDateTime.currentDateTime().toString('yyMMddhhmmss')
            fileName = str(self.page) # 以页码为图片名
            logger.debug('filePath %s', os.path.join(self.filePath, 'temp', fileName + '.png'))
            self.pix.save(os.path.join(self.filePath, 'temp', fileName + '.png'))
            logger.debug('保存图片')

            # 2.保存保存路径json文件到本地
            import json
            dict = {'pox_xyc': self.pos_xyc,
                    'page': self.page,
                    'meetingID': self.meetingID
                    }
            # logger.debug('dict: %s', dict)

            with open(os.path.join(self.filePath, 'temp', fileName + '.json'), 'w') as f:
                json.dump(dict, f)
            logger.debug('保存json文件')

        else:

            # 用户手动保存
            fileName = QFileDialog.getSaveFileName(self, '保存图片', self.filePath, ".png;;.jpg")
            self.pix.save(fileName[0] + fileName[1])

    def clearScree(self):
        '''清屏'''

        # self.pos_xyc.clear()
        self.update()
        self.pix.fill(Qt.white)

    def closeEvent(self):
        '''
        关闭白板时保存当前画板内容
        :return:
        '''
        logger.debug('关闭事件')
        if self.isWritten:
            self.savePicture(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dbb = DrawingBoardUIBusi()
    # dbb.setupBusi()
    # dbb.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint)
    dbb.showMaximized()
    sys.exit(app.exec_())
