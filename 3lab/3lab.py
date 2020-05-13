import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon  
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64  
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore import Qt
from math import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QPoint
import time
from math import *
import numpy as np

def sign(x):
    if x == 0:
        return 0
    else:
        return x/abs(x)


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radioButton.setChecked(1)
        self.colourLine = Qt.black
        self.colourCanvas = Qt.white
        self.flag = None
        self.startPointX = 0
        self.startPointY = 0
        self.endPointX = 0
        self.endPointY = 0
        self.radio = 1
        self.pushButton_2.clicked.connect(self.drawCircle)
        self.pushButton_3.clicked.connect(self.clickBtnWhiteCanv)
        self.pushButton_4.clicked.connect(self.clickBtnBlackCanv)
        self.pushButton_5.clicked.connect(self.clickBtnBlueCanv)
        self.pushButton_6.clicked.connect(self.clickBtnRedCanv)
        self.pushButton_8.clicked.connect(self.clickBtnWhiteLine)
        self.pushButton_7.clicked.connect(self.clickBtnBlackLine)
        self.pushButton_9.clicked.connect(self.clickBtnBlueLine)
        self.pushButton_10.clicked.connect(self.clickBtnRedLine)
        self.pushButton.clicked.connect(self.clckBtnDrawLine)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 1115, 621)
        self.graphicsView.setScene(self.scene)
        #self.image.fill(self.colourCanvas)
        self.scene.setBackgroundBrush(self.colourCanvas)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pen = QPen()
        self.pen.setWidth(3)
        self.pen.setColor(self.colourLine)
        self.pushButton_11.clicked.connect(self.clearScene)
        self.pushButton_12.clicked.connect(self.changeWidth)
        self.width = 1115
        self.height = 621
        self.widthForSun = 0
        self.angleForSun = 0

    def changeWidth(self):
        try:
            new = int(self.lineEdit_7.text())
            self.pen.setWidth(new)
        except:
            pass

    def clearScene(self):
        self.scene.clear()

    def clickBtnWhiteCanv(self):
        self.colourCanvas = Qt.white
        self.scene.setBackgroundBrush(self.colourCanvas)
    def clickBtnBlackCanv(self):
        self.colourCanvas = Qt.black
        self.scene.setBackgroundBrush(self.colourCanvas)
    def clickBtnBlueCanv(self):
        self.colourCanvas = Qt.blue
        self.scene.setBackgroundBrush(self.colourCanvas)
    def clickBtnRedCanv(self):
        self.colourCanvas = Qt.red    
        self.scene.setBackgroundBrush(self.colourCanvas)
    def clickBtnWhiteLine(self):
        self.colourLine = Qt.white
        self.pen.setColor(self.colourLine)
    def clickBtnBlackLine(self):
        self.colourLine = Qt.black
        self.pen.setColor(self.colourLine)
    def clickBtnBlueLine(self):
        self.colourLine = Qt.blue
        self.pen.setColor(self.colourLine)
    def clickBtnRedLine(self):
        self.colourLine = Qt.red
        self.pen.setColor(self.colourLine)

    def clckBtnDrawLine(self):
        try:
            startX = float(self.lineEdit.text())
            startY = float(self.lineEdit_2.text())
            endX = float(self.lineEdit_3.text())
            endY = float(self.lineEdit_4.text())

            self.startPointX = startX
            self.startPointY = startY
            self.endPointX = endX
            self.endPointY = endY

            self.checkRadio()

            self.flag = 'Line'
            self.drawEvent()

        except:
            pass

    def checkRadio(self):
        if self.radioButton.isChecked():
            self.radio = 1
        elif self.radioButton_2.isChecked():
            self.radio = 2
        elif self.radioButton_3.isChecked():
            self.radio = 3
        elif self.radioButton_4.isChecked():
            self.radio = 4
        elif self.radioButton_5.isChecked():
            self.radio = 5
        elif self.radioButton_6.isChecked():
            self.radio = 6

    def drawLineLibrary(self):
        self.scene.addLine(self.startPointX, self.startPointY, self.endPointX, self.endPointY, self.pen)

    def setPixel(self, x, y):
        self.scene.addLine(x, y, x, y, self.pen)

    def abs(self, x):
        return round(x)

    def drawLineCDA(self):
        self.pen.setColor(self.colourLine)
        x1 = (self.startPointX)
        x2 = (self.endPointX)
        y1 = (self.startPointY) 
        y2 = (self.endPointY)

        length = max(abs(x1 - x2), abs(y1 - y2))

        if length == 0:
            self.setPixel(x1, y1)
        else:
            dX = (x2 - x1) / length
            dY = (y2 - y1) / length

            x = x1
            y = y1

            while length > 0:
                self.setPixel(self.abs(x), self.abs(y))
                x += dX 
                y += dY
                length -= 1

    def drawLineBrz(self):
        x1 = (self.startPointX)
        x2 = (self.endPointX)
        y1 = (self.startPointY) 
        y2 = (self.endPointY)
        if x1 == x2 and y1 == y2:
            self.setPixel(x1, y1)
        else:
            dx = x2 - x1
            dy = y2 - y1
            sx = sign(dx)
            sy = sign(dy)
            dx = abs(dx)
            dy = abs(dy)
            x = x1
            y = y1
            change = False
            if dy > dx:
                dx, dy = dy, dx
                change = True
            h = dy / dx
            e = h - 0.5
            i = 0
            while i <= dx:
                self.setPixel(x, y)
                if e >= 0:
                    if change is False:
                        y += sy
                    else:
                        x += sx
                    e -= 1

                if e < 0:
                    if change is False:
                        x += sx
                    else:
                        y += sy
                    e += h
                i+=1

    def drawLineBri(self):
        x1 = (self.startPointX)
        x2 = (self.endPointX)
        y1 = (self.startPointY) 
        y2 = (self.endPointY)
        if x1 == x2 and y1 == y2:
            self.setPixel(x1, y1)
        else:
            dx = x2 - x1
            dy = y2 - y1
            sx = sign(dx)
            sy = sign(dy)
            dx = abs(dx)
            dy = abs(dy)
            x = x1
            y = y1

            change = False
            if dy > dx:
                temp = dx
                dx = dy
                dy = temp
                change = True
            e = 2 * dy - dx
            i = 1
            while i <= dx:
                self.setPixel(x, y)
                if e >= 0:
                    if change == 0:
                        y += sy
                    else:
                        x += sx
                    e -= 2 * dx

                if e < 0:
                    if change == 0:
                        x += sx
                    else:
                        y += sy
                    e += (2 * dy)
                i += 1

    def drawLineSoft(self):
        x1 = (self.startPointX)
        x2 = (self.endPointX)
        y1 = (self.startPointY) 
        y2 = (self.endPointY)
        if x1 == x2 and y1 == y2:
            self.setPixel(x1, y1)
        else:
            dx = x2 - x1
            dy = y2 - y1
            sx = sign(dx)
            sy = sign(dy)
            dx = abs(dx)
            dy = abs(dy)
            x = x1
            y = y1

            change = False

            if dy > dx:
                dx, dy = dy, dx
                change = True
            

            i_max = 255
            h = i_max * dy / dx
            e = i_max/2
            w = i_max - h
            i = 1
            while i <= dx:
                if e < w:
                    if change:
                        y += sy
                    else:
                        x += sx
                    e += h
                else:
                    x += sx
                    y += sy
                    e -= w
                new = QColor()
                new.setAlpha(255 - e)
                self.pen.setColor(new)

                self.setPixel(x, y)
                i += 1

    def changeColorWu(self, i_max, y):
        new = QColor()
        new.setAlpha(i_max - i_max * (fabs(y - int(y))))
        self.pen.setColor(new)

    def drawLineWu(self):
        x1 = (self.startPointX)
        x2 = (self.endPointX)
        y1 = (self.startPointY) 
        y2 = (self.endPointY)
        if x1 == x2 and y1 == y2:
            self.scene.addLine(x1, y1, x1, y1, self.pen)
        else:
            xb = x1
            yb = y1
            xe = x2
            ye = y2
            dx = x2 - x1
            dy = y2 - y1
            change = abs(dx) < abs(dy)

            if change:
                xb, yb = yb, xb
                xe, ye = ye, xe
                dx, dy = dy, dx

            if xe < xb:
                xb, xe = xe, xb
                yb, ye = ye, yb
            grad = 0
            if dy != 0:
                grad = dy / dx

            y = yb
            x = xb
            i_max = 255
            while x <= xe:
                if change:
                    s = sign(y)
                    self.changeColorWu(i_max, y)
                    self.setPixel(y, x)

                    if dy and dx:            
                        self.changeColorWu(i_max, y)
                        self.setPixel(y, x)

                    self.setPixel(y + s, x)
                else:
                    s = sign(y)
                    self.changeColorWu(i_max, y)
                    self.setPixel(x, y)

                    if dy and dx:
                        self.changeColorWu(i_max, y)
                        self.setPixel(x, y)
                    self.setPixel(x, y + s)
                y += grad

                x += 1


    def drawLineManager(self):
        self.checkRadio()
        self.image.fill(self.colourCanvas)
        if self.radio == 1:
            self.drawLineLibrary()
        elif self.radio == 2:
            self.drawLineCDA()
        elif self.radio == 3:
            self.drawLineBrz()
        elif self.radio == 4:
            self.drawLineBri()
        elif self.radio == 5:
            self.drawLineSoft()
        elif self.radio == 6:
            self.drawLineWu()

    def drawCircle(self):
        try:
            self.widthForSun = float(self.lineEdit_5.text())
            self.angleForSun = int(self.lineEdit_6.text())
        except:
            pass
        finally:
            self.checkRadio()
            print(self.radio)
            self.startPointX = self.width / 2
            self.startPointY = self.height / 2
            for i in np.arange(0, 360, self.angleForSun):
                self.endPointX = cos(radians(i)) * self.widthForSun + self.width / 2
                self.endPointY = sin(radians(i)) * self.widthForSun + self.height / 2
                self.checkRadio()
                if self.radio == 1:
                    self.drawLineLibrary()
                elif self.radio == 2:
                    self.drawLineCDA()
                elif self.radio == 3:
                    self.drawLineBrz()
                elif self.radio == 4:
                    self.drawLineBri()
                elif self.radio == 5:
                    self.drawLineSoft()
                else:
                    self.drawLineWu()
    
    def paintEvent(self, event):
        self.painter = QPainter(self)
        if self.flag == 'Line':
            self.painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
            self.drawLineManager()
            self.flag = None

        brush = QBrush(Qt.gray)
        self.painter.setBrush(brush)
        self.painter.drawRect(0,621,1115,788)
        self.painter.end()

    def drawEvent(self):
        if self.flag == 'Line':
            self.drawLineManager()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()