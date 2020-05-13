import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets  
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QTableWidgetItem
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF
from math import *
import time
from numpy import sign

colBackground = Qt.white
flag = 0

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = myScene(0, 0, 871, 601)
        self.graphicsView.setScene(self.scene)
        self.scene.setBackgroundBrush(Qt.white)
        self.image = QImage(871, 601, QImage.Format_ARGB32_Premultiplied)
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
        self.pushButton_5.clicked.connect(self.changeFlag)
        self.curMasX = []
        self.curMasY = []
        self.pixX = None
        self.pixY = None

    def changeFlag(self):
        global flag
        flag = 1

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

    def addPix(self, point):
        self.pixX = int(point.x())
        self.pixY = int(point.y())
        self.label_9.setText('x=' + str(self.pixX) + '   ' + 'y=' + str(self.pixY))


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

    def start(self):
        self.radioManager()
        self.drawEdges()
        self.fillFigure()
        self.drawEdgesEnd()
        pix = QPixmap()
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)

    def radioManager(self):
        if self.radioButton.isChecked():
            self.colFill = Qt.black
        elif self.radioButton_2.isChecked():
            self.colFill = Qt.gray
        elif self.radioButton_3.isChecked():
            self.colFill = Qt.red
        else:
            self.colFill = Qt.blue

    def drawBorders(self, myPainter):
        myPainter.drawLine(2, 2, 868, 2)
        myPainter.drawLine(868, 2, 868, 598)
        myPainter.drawLine(868, 598, 2, 598)
        myPainter.drawLine(2, 2, 2, 598)

    def drawEdgesEnd(self):
        for i in range(len(self.masX)):
            self.curMasX = self.masX[i]
            self.curMasY = self.masY[i]
            edge = self.colFill
            myPainter = QPainter()
            myPainter.begin(self.image)
            myPainter.setPen(QPen(edge))
            for i in range(len(self.curMasX) - 1):
                myPainter.drawLine(self.curMasX[i], self.curMasY[i], self.curMasX[i + 1], self.curMasY[i + 1])
            myPainter.drawLine(self.curMasX[len(self.curMasX) - 1], self.curMasY[len(self.curMasX) - 1], self.curMasX[0], self.curMasY[0])
            self.drawBorders(myPainter)
            myPainter.end()

    def drawEdges(self):
        for i in range(len(self.masX)):
            self.curMasX = self.masX[i]
            self.curMasY = self.masY[i]
            edge = Qt.darkYellow
            myPainter = QPainter()
            myPainter.begin(self.image)
            myPainter.setPen(QPen(edge))
            for i in range(len(self.curMasX) - 1):
                myPainter.drawLine(self.curMasX[i], self.curMasY[i], self.curMasX[i + 1], self.curMasY[i + 1])
            myPainter.drawLine(self.curMasX[len(self.curMasX) - 1], self.curMasY[len(self.curMasX) - 1], self.curMasX[0], self.curMasY[0])
            self.drawBorders(myPainter)
            myPainter.end()

    def fillFigure(self):
        pix = QPixmap()

        paint = QPainter()
        paint.begin(self.image)

        borders = Qt.darkYellow
        paint.setPen(QPen(self.colFill))

        stack = []
        stack.append([self.pixX, self.pixY])
        startTime = time.time()
        while stack:
            # извлечение пикселя (х,у) из стека
            curPoint = stack.pop()
            x = curPoint[0]
            y = curPoint[1]
            paint.drawPoint(x, y)
            # сохраняем x-координату затравочного пиксела
            temporaryX = curPoint[0]

            # заполняем интервал справа от затравки
            x = x + 1
            while QColor(self.image.pixel(x, y)) != borders:
                paint.drawPoint(x, y)
                x = x + 1
            # сохраняем крайний справа пиксел
            xr = x - 1
            # восстанавливаем x-координату затравки
            x = temporaryX
            
            # заполняем интервал слева от затравки
            x = x - 1
            while QColor(self.image.pixel(x, y)) != borders:
                paint.drawPoint(x, y)
                x = x - 1
            # сохраняем крайний справа пиксел
            xl = x + 1

            y = y + 1
            x = xl
            while x <= xr:
                # ищем затравку на строке выше
                flag = 0
                while QColor(self.image.pixel(x, y)) != borders and  \
                    QColor(self.image.pixel(x, y)) != self.colFill and  x <= xr:
                    if flag == 0:
                        flag = 1
                    x = x + 1

                # помещаем в стек крайний справа пиксел
                if flag == 1:
                    if x == xr and QColor(self.image.pixel(x, y)) != borders and \
                        QColor(self.image.pixel(x, y)) != self.colFill:
                        stack.append([x, y])
                    else:
                        stack.append([x - 1, y])
                    flag = 0
                # продолжим проверку, если интервал был прерван
                temporaryX = x
                while (QColor(self.image.pixel(x, y)) == borders or \
                    QColor(self.image.pixel(x, y)) == self.colFill) and x < xr:
                    x = x + 1

                # удостоверимся, что координата пиксела увеличена
                if x == temporaryX:
                    x = x + 1
            # проверяем строку ниже
            y = y - 2
            x = xl
            while x <= xr:
                flag = 0
                while QColor(self.image.pixel(x, y)) != borders and \
                    QColor(self.image.pixel(x, y)) != self.colFill and x <= xr:
                    if flag == 0:
                        flag = 1
                    x = x + 1


                if flag == 1:
                    if x == xr and QColor(self.image.pixel(x, y)) != self.colFill and \
                        QColor(self.image.pixel(x, y)) != borders:
                        stack.append([x, y])
                    else:
                        stack.append([x - 1, y])
                    flag = 0

                temporaryX = x
                while (QColor(self.image.pixel(x, y)) == borders or \
                    QColor(self.image.pixel(x, y)) == self.colFill) and x < xr:
                    x = x + 1

                if x == temporaryX:
                    x = x + 1
            
            if self.checkBox.isChecked():
                self.delay()
                pix.convertFromImage(self.image)
                self.scene.addPixmap(pix)
        endTime = time.time()
        self.label_7.setText(str(round(endTime - startTime, 3)))

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
        global flag
        if not flag:
            point = event.scenePos()
            window.addElem(point)
        else:
            point = event.scenePos()
            flag = 0
            window.addPix(point)
            

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

