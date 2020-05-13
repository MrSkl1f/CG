import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets  
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QTableWidgetItem
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
from math import *
import time
from numpy import sign

colBackground = Qt.white

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = myScene(170, 0, 951, 601)
        self.graphicsView.setScene(self.scene)
        self.scene.setBackgroundBrush(Qt.white)
        self.image = QImage(1121, 601, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(colBackground)
        self.radioButton.setChecked(1)
        self.pointNow = None
        self.colFill = Qt.black
        self.pen = QPen()
        self.pen.setWidth(1)
        self.pen.setColor(Qt.black)
        self.masX = []
        self.masY = []
        self.flag = 0
        self.pushButton.clicked.connect(self.addByDoubleBoxes)
        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_4.clicked.connect(self.drawLastLine)
        self.pushButton_3.clicked.connect(self.clearScene)
        self.curMasX = []
        self.curMasY = []

    def addByDoubleBoxes(self):
        try:
            x = int(self.doubleSpinBox.value())
            y = int(self.doubleSpinBox_2.value())
        except:
            pass
        finally:
            self.listWidget.addItem('( ' + str(x) + ' ; ' + str(y) + ' )')
            if self.flag == 0:
                self.masX.append([int(x)])
                self.masY.append([int(y)])
                self.flag = 1
            else:
                self.masX[len(self.masX) - 1].append(int(x))
                self.masY[len(self.masY) - 1].append(int(y))
            self.drawCurLine()

    def clearScene(self):
        self.scene.clear()
        self.image = QImage(1121, 601, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(colBackground)
        self.masX = []
        self.masY = []
        self.flag = 0
        self.pointNow = None
        self.listWidget.clear()

    def addElem(self, point):
        self.listWidget.addItem('( ' + str(point.x()) + ' ; ' + str(point.y()) + ' )')
        if self.flag == 0:
            self.masX.append([int(point.x())])
            self.masY.append([int(point.y())])
            self.flag = 1
        else:
            self.masX[len(self.masX) - 1].append(int(point.x()))
            self.masY[len(self.masY) - 1].append(int(point.y()))
        self.drawCurLine()

    def drawCurLine(self):
        length = len(self.masX[len(self.masX) - 1])
        if length > 1:
            self.scene.addLine(self.masX[len(self.masX) - 1][length - 1], self.masY[len(self.masX) - 1][length - 1], self.masX[len(self.masX) - 1][length - 2], self.masY[len(self.masX) - 1][length - 2])

    def drawLastLine(self):
        length = len(self.masX[len(self.masX) - 1])
        if length > 1:
            self.scene.addLine(self.masX[len(self.masX) - 1][0], self.masY[len(self.masX) - 1][0], self.masX[len(self.masX) - 1][length - 1], self.masY[len(self.masX) - 1][length - 1])        
            self.flag = 0
        print(self.masX)

    def delay(self):
        QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)


    def drawLineBri(self, myPainter, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            myPainter.drawPoint(x1, y1)
        elif y1 == y2:
            print('yes')
            pass
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
            i = 0
            lastY = y1
            # Если пиксел уже стоит - ставим соседний
            if QColor(self.image.pixel(x, y)) == self.colFill:
                myPainter.drawPoint(x + 1, y)
            else:
                myPainter.drawPoint(QPoint(x, y))     

            while i < dx:
                # Проверка - если линия совпадает с предыдущей, то пропускаем 
                if y != lastY:
                    # Если пиксел уже стоит - ставим соседний
                    if QColor(self.image.pixel(x, y)) == self.colFill:
                        myPainter.drawPoint(x + 1, y)
                    else:
                        myPainter.drawPoint(x, y)  
                    lastY = y
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
                if y == y2:
                    break
            #if QColor(self.image.pixel(x2, y2)) != self.colFill:
            #    myPainter.drawPoint(x2, y2)

    def start(self):
        self.radioManager()
        if self.checkBox.isChecked():
            self.fillFigure()
        else:
            self.fillWithFlag()

    def radioManager(self):
        if self.radioButton.isChecked():
            self.colFill = Qt.black
        elif self.radioButton_2.isChecked():
            self.colFill = Qt.gray
        elif self.radioButton_3.isChecked():
            self.colFill = Qt.red
        else:
            self.colFill = Qt.blue

    def fillFigure(self):
        pix = QPixmap()
        myPainter = QPainter()
        # Находим граничные значения фигуры
        xMax, xMin = self.findMaxMinX()
        yMax, yMin = self.findMaxMinY()
        # Отрисовываем границы
        self.drawEdges()
        
        # Скан линии от нижней границы к верхней 
        for y in range(yMin, yMax, 1):
            myPainter.begin(self.image)
            # Изначально значение flag = false, т.е. мы не начали и не закончили закраску
            flag = False
            for x in range(xMin, xMax, 1):
                # Как только встречаем пиксел цвета закраски - меняем флаг (заканчиваем или начинаем закраску)
                if QColor(self.image.pixel(x, y)) == self.colFill:
                    if flag == False:
                        flag = True
                        myPainter.setPen(QPen(self.colFill))
                    else:
                        flag = False     
                # Если флаг True, то мы ставим пиксел цвета закраски
                if flag == True:
                    myPainter.setPen(QPen(self.colFill))
                else:
                    myPainter.setPen(QPen(colBackground))
                myPainter.drawPoint(x, y)
        
            if self.checkBox.isChecked():
                self.delay()
                pix.convertFromImage(self.image)
                self.scene.addPixmap(pix)
            myPainter.end()
        if not self.checkBox.isChecked():
            self.delay()
            pix.convertFromImage(self.image)
            self.scene.addPixmap(pix)

    def fillWithFlag(self):
        pix = QPixmap()
        myPainter = QPainter()

        xMax, xMin = self.findMaxMinX()
        yMax, yMin = self.findMaxMinY()
        self.drawEdges()
        
        startTime = time.time()
        for y in range(yMin, yMax, 1):
            flag = False
            myPainter.begin(self.image)
            for x in range(xMin, xMax, 1):
                if QColor(self.image.pixel(x, y)) == self.colFill:
                    if flag == False:
                        flag = True
                        myPainter.setPen(QPen(self.colFill))
                    else:
                        flag = False     
                if flag == True:
                    myPainter.setPen(QPen(self.colFill))
                else:
                    myPainter.setPen(QPen(colBackground))
                
                myPainter.drawPoint(x, y)
            myPainter.end()
        endTime = time.time()
        
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)
        self.label_7.setText(str(round(endTime - startTime, 3)))

    def checkExtreme(self, myPainter):
        for i in range(1, len(self.curMasX) - 1, 1):
            if (self.curMasY[i] < self.curMasY[i - 1] and self.curMasY[i] < self.curMasY[i + 1]) or (self.curMasY[i] > self.curMasY[i - 1] and self.curMasY[i] > self.curMasY[i + 1]):
                myPainter.drawPoint(self.curMasX[i] + 1, self.curMasY[i])
                myPainter.drawPoint(self.curMasX[i], self.curMasY[i])

        if (self.curMasY[len(self.curMasX) - 1] < self.curMasY[0] and self.curMasY[len(self.curMasX) - 1] < self.curMasY[len(self.curMasX) - 2]) or (self.curMasY[len(self.curMasX) - 1] > self.curMasY[0] and self.curMasY[len(self.curMasX) - 1] > self.curMasY[len(self.curMasX) - 2]):
            myPainter.drawPoint(self.curMasX[len(self.curMasX) - 1] + 1, self.curMasY[len(self.curMasX) - 1])
            myPainter.drawPoint(self.curMasX[len(self.curMasX) - 1], self.curMasY[len(self.curMasX) - 1])

        if (self.curMasY[0] < self.curMasY[len(self.curMasX) - 1] and self.curMasY[0] < self.curMasY[1]) or (self.curMasY[0] > self.curMasY[len(self.curMasX) - 1] and self.curMasY[0] > self.curMasY[1]):
            myPainter.drawPoint(self.curMasX[0] + 1, self.curMasY[0])
            myPainter.drawPoint(self.curMasX[0], self.curMasY[0])

    def drawEdges(self):
        for i in range(len(self.masX)):
            self.curMasX = self.masX[i]
            self.curMasY = self.masY[i]
            myPainter = QPainter()
            myPainter.begin(self.image)
            myPainter.setPen(QPen(self.colFill))
            self.checkExtreme(myPainter)
            for i in range(len(self.curMasX) - 1):
                self.drawLineBri(myPainter, self.curMasX[i], self.curMasY[i], self.curMasX[i + 1], self.curMasY[i + 1])
            self.drawLineBri(myPainter, self.curMasX[len(self.curMasX) - 1], self.curMasY[len(self.curMasX) - 1], self.curMasX[0], self.curMasY[0])
            myPainter.end()

    def findMaxMinX(self):
        xMax = None
        xMin = None
        for i in range(len(self.masX)):
            for j in range(len(self.masX[i])):
                if xMax is None or self.masX[i][j] > xMax:
                    xMax = self.masX[i][j]
                if xMin is None or self.masX[i][j] < xMin:
                    xMin = self.masX[i][j]
        return xMax, xMin

    def findMaxMinY(self):
        yMax = None
        yMin = None
        for i in range(len(self.masY)):
            for j in range(len(self.masX[i])):
                if yMax is None or self.masY[i][j] > yMax:
                    yMax = self.masY[i][j]
                if yMin is None or self.masY[i][j] < yMin:
                    yMin = self.masY[i][j]
        return yMax, yMin

class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        global window
        point = event.scenePos()
        window.addElem(point)


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

