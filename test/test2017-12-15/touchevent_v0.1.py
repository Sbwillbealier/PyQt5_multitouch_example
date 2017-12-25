import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QPixmap, QPen, QTouchEvent, QColor
from PyQt5.QtCore import Qt, QPoint, QEvent, QCoreApplication, QPointF, QLineF
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        # self.setWindowTitle("绘图例子")
        self.lastPoint_t = QPointF()  # 触屏点前一点
        self.endPoint_t = QPointF()  # 触屏点后一点
        self.lastPoint_m = QPointF()  # 鼠标点前一点
        self.endPoint_m = QPointF()  # 鼠标点后一点

        self.pix = QPixmap()  # 画布

        self.pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  # 画笔
        self.pen.setColor(QColor(0, 0, 0))  # 设置初始颜色
        self.cp = QDesktopWidget().availableGeometry()  # 分辨率
        self.init()

    def init(self):

        # 设置接受触摸屏
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        QCoreApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents, False)

        # 窗口大小设置为800*600
        self.resize(self.cp.width() * 0.9, self.cp.height() * 0.9)

        # 画布大小为400*400，背景为白色
        self.pix = QPixmap(self.cp.width(), self.cp.height())

        self.pix.fill(Qt.white)

        self.pp = QPainter(self.pix)
        self.pp.setPen(self.pen)

        self.lines = []

    def paintEvent(self):
        logger.debug('开始绘制')
        # 根据鼠标指针前后两个位置绘制直线
        distance = int(
            math.sqrt(
                (self.lastPoint_m.x() - self.endPoint_m.x()) ** 2 + (
                    self.lastPoint_m.y() - self.endPoint_m.y()) ** 2)) + 1

        # print('distance', distance)

        # self.pp.drawLine(self.lastPoint_m, self.endPoint_m)
        self.pp.begin(self.pix)
        self.drawLines(distance, self.lastPoint_m, self.endPoint_m)
        self.pp.end()
        # self.pix.save('1.png') # 保存图片

        # self.pp.drawPoints(self.lastPoint,self.endPoint)
        self.lastPoint_m = self.endPoint_m

        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.drawPixmap(0, 0, self.pix)
        # print('画在窗体上')

    def paintTouchEvent(self):

        # 根据触摸点前后两个位置绘制直线
        distance = int(
            math.sqrt(
                (self.lastPoint_t.x() - self.endPoint_t.x()) ** 2 + (
                    self.lastPoint_t.y() - self.endPoint_t.y()) ** 2)) + 1

        print('distance', distance)
        distance = math.sqrt(distance)
        if distance > 6:
            distance = 6
        elif distance < 4:
            distance = 4;
        self.pen.setWidthF(18 / distance)
        self.pp.setPen(self.pen)
        self.pp.drawLine(self.lastPoint_t, self.endPoint_t)
        # self.pix.save('1.png') # 保存图片

        # self.pp.drawPoints(self.lastPoint,self.endPoint)

        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.drawPixmap(0, 0, self.pix)
        # print('画在窗体上')

    def mousePressEvent(self, event):
        # 鼠标左键按下
        if event.button() == Qt.LeftButton:
            # print('左键按下')
            self.lastPoint_m = event.pos()
            self.endPoint_m = self.lastPoint_m

    def mouseMoveEvent(self, event):
        # 鼠标左键按下的同时移动鼠标
        # print(QEvent.TouchBegin)

        if event.buttons() and Qt.LeftButton:
            self.endPoint_m = event.pos()
            # 进行重新绘制
            self.update()

    def mouseReleaseEvent(self, event):
        # 鼠标左键释放
        if event.button() == Qt.LeftButton:
            self.endPoint_m = event.pos()
            # 进行重新绘制
            self.update()

    def eventFilter(self, watched, event):
        '''
        事件过滤器
        :param watched: 监听到的对象
        :param event: 事件
        :return: 符合条件的事件单独处理，否则交给父类处理
        '''
        # print(type(watched))
        if watched == form:
            # print('watched==form')
            # print(event.type())
            if event.type() == QEvent.TouchBegin:
                pass
            if event.type() == QEvent.TouchUpdate or event.type() == QEvent.TouchEnd:
                # print('触点开始', QTouchEvent(event).touchPoints())
                logger.debug('TouchEvent')
                self.addline(QTouchEvent(event))

            if event.type() == QEvent.Paint:
                logger.debug('PaintEvent')
                self.paintEvent()
                # self.update()
                return True
        return QWidget.eventFilter(self, watched, event)  # 其他情况会返回系统默认的事件处理方法。

    # def event(self, event):
    #     if event.type() == QEvent.TouchBegin:
    #         return True
    #     if event.type() == QEvent.TouchBegin or event.type() == QEvent.TouchUpdate or event.type() == QEvent.TouchEnd:
    #         # print('触点开始', QTouchEvent(event).touchPoints())
    #         # self.addline(QTouchEvent(event))
    #         return True
    #
    #     return QWidget.event(self, event)


    def addline(self, event):
        '''
        获取触摸点
        :param event: 触摸事件对象
        :return:
        '''
        touchPoints = event.touchPoints()
        for point in touchPoints:
            logger.debug('触摸点的直径：', point.ellipseDiameters())
            logger.debug('触摸点的压力：', point.pressure())
            logger.debug('触摸点的状态：', point.state())
            self.lastPoint_t = point.lastPos()
            self.endPoint_t = point.pos()
            print('lastPoint', self.lastPoint_t)
            print('endPoint', self.endPoint_t)
            line = QLineF()
            line.setP1(self.lastPoint_t)
            line.setP2(self.lastPoint_t)
            self.lines.append(line)
            self.paintTouchEvent()  # 手动调绘图事件
        self.update()  #

    def drawLines(self, distance, startPoint, endPoint):
        '''

        :param distance:
        :param startPoint:
        :param endPoint:
        :return:
        '''
        distance_sqrt = math.sqrt(distance)
        if distance_sqrt > 8:
            distance_sqrt = 6
        elif distance_sqrt < 4:
            distance_sqrt = 4;
        print(distance)
        if distance > 40:
            self.pen.setColor(QColor(40, 40, 40))  # 设置初始颜色
        else:
            self.pen.setColor(QColor(distance, distance, distance))  # 设置初始颜色


        self.pen.setWidthF(25 / distance_sqrt)  # 设置笔宽
        self.pp.setPen(self.pen)
        points = []
        points.append(startPoint)

        num_add_point = 10
        add_x = endPoint.x() - startPoint.x()
        add_y = endPoint.y() - startPoint.y()
        for i in range(1, num_add_point + 1):
            points.append(
                QPointF(startPoint.x() + i * add_x / num_add_point, startPoint.y() + i * add_y / num_add_point))

        points.append(endPoint)
        for i in range(num_add_point + 1):
            # print(points[i])
            self.pp.drawLine(points[i], points[i + 1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C:
            self.pix.fill(Qt.white)
            self.update()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    app.installEventFilter(form)  # 监听form的所有事件
    form.show()
    form.showMaximized()
    sys.exit(app.exec_())
