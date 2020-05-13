import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon    
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore import Qt
from math import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QPoint
import time

def func(x):
    return x

def findMoves(xCircle, yCircle):
    UpperX, UpperY, LowerX, LowerY = findUppers(xCircle, yCircle)
    centerX = (UpperX + LowerX) / 2
    centerY = (UpperY + LowerY) / 2
    moveX = (721 / 2 - centerX)
    moveY = (461 / 2 - centerY)
    return moveX, moveY

def findUppers(xCircle, yCircle):
    upX = xCircle[0]
    upY = yCircle[0]
    loX = xCircle[0]
    loY = yCircle[0]
    for i in range(len(xCircle)):
        if xCircle[i] > upX:
            upX = xCircle[i]
        if xCircle[i] < loX:
            loX = xCircle[i]
        if yCircle[i] > upY:
            upY = yCircle[i]
        if yCircle[i] < loY:
            loY = yCircle[i]
    return upX, upY, loX, loY

def findMashtab(xCircle, yCircle, xGip, yGip, a, b):
    upX, upY, loX, loY = findUppers(xCircle, yCircle)
    coefX = floor(float(721 - 2 * 30) / float(upX - loX))
    coefY = floor(float(461 - 2 * 30) / float(upY - loY))
    mashtab = min(coefX, coefY)
    for i in range(len(xCircle)):
        xCircle[i] *= mashtab
        yCircle[i] *= mashtab
    for i in range(len(xGip)):
        xGip[i] *= mashtab
        yGip[i] *= mashtab
    return xCircle, yCircle, xGip, yGip

def createMass(a, b, c, r):
    xCircle = []
    yCircle = []
    xGip = []
    yGip = []
    t = 0
    div = 1000
    for i in range(2000):
        xCircle.append(r * cos(t) + a)
        yCircle.append(r * sin(t) + b)
        t += pi / div

    for i in range(len(xCircle)):
        if xCircle[i] > -1e-5 and xCircle[i] < 1e-5:
            xCircle[i] -= 1e-5
        if (c / xCircle[i] <= yCircle[i]) and (xCircle[i] - a) ** 2 + (c / xCircle[i] - b) ** 2 <= r ** 2 and c / xCircle[i] > 0:
            xGip.append(xCircle[i])
            yGip.append(c / xCircle[i])    
    for i in range(len(xCircle)):
        if xCircle[i] > -1e-5 and xCircle[i] < 1e-5:
            xCircle[i] -= 1e-5    

    index = 0
    for i in range(len(xCircle) - 1):
        if yCircle[i] < c / xCircle[i] and xCircle[i] > 0 and \
            yCircle[i + 1] >= c / xCircle[i] and xCircle[i + 1] > 0:
            index = i + 1
            break

    checkX = []
    checkY = []
    i = index
    for j in range(len(xCircle)):
        if i == len(xCircle):
            i = 0
        if yCircle[i] >= c / xCircle[i] and xCircle[i] > 0:
            checkX.append(xCircle[i])
            checkY.append(yCircle[i])
        i += 1
    
    for i in range(len(xGip)-1):
        for j in range(len(xGip)-i-1):
            if xGip[j] > xGip[j+1]:
                xGip[j], xGip[j+1] = xGip[j+1], xGip[j]
                yGip[j], yGip[j+1] = yGip[j+1], yGip[j]

    return checkX, checkY, xGip, yGip

def check(arrX, arrY, i, j, moveX, moveY):
    if 10 <= 10 + arrX[i] + moveX <= 741 and \
        10 <= 481 - (10 + arrY[i] + moveY) <= 471 and \
        10 <= 10 + arrX[j] + moveX <= 741 and \
        10 <= 481 - (10 + arrY[j] + moveY) <= 471:
        return 1
    else:
        return 0

def checkSecond(arrX, arrY, arrsX, arrsY, i, j, moveX, moveY):
    if 10 <= 10 + arrX[i] + moveX <= 741 and \
        10 <= 481 - (10 + arrY[i] + moveY) <= 471 and \
        10 <= 10 + arrsX[j] + moveX <= 741 and \
        10 <= 481 - (10 + arrsY[j] + moveY) <= 471:
        return 1
    else:
        return 0

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.a = 1
        self.b = 1
        self.c = 1
        self.r = 1
        self.xCircle = []
        self.yCircle = []
        self.xGip = []
        self.yGip = []
        self.massX = []
        self.massY = []
        self.X = [365.5, 10, 365.5, 471]
        self.Y = [10, 240.5, 741, 240.5]
        if True:
            self.lineEdit.setText('1')
            self.lineEdit_2.setText('1')
            self.lineEdit_3.setText('1')
            self.lineEdit_4.setText('1')
            self.lineEdit_5.setText('1')
            self.lineEdit_6.setText('1')
        self.moveX = 0
        self.moveY = 0
        self.lastParamFirst = None
        self.lastParamSecond = None
        self.lastParamThird = None
        self.lastParamFourth = None

        self.flag = None
        self.flagForReturn = None

        self.pushButton.clicked.connect(self.clickBtnAdd)
        self.pushButton_3.clicked.connect(self.returnBack)
        self.pushButton_2.clicked.connect(self.createPic)
        self.pushButton_4.clicked.connect(self.movePic)
        self.pushButton_5.clicked.connect(self.mashtabPic)
        self.pushButton_6.clicked.connect(self.turnPic)

    def returnBack(self):
        if self.flagForReturn == 'Move':
            self.converForMove(0-(self.lastParamFirst), 0-(self.lastParamSecond))
            self.flag = 'Create'
            self.flagForReturn = None
            self.update()
        elif self.flagForReturn == 'Mashtab':
            self.converForMashtab(1 / self.lastParamFirst, 1 / self.lastParamSecond, self.lastParamThird, self.lastParamFourth)
            self.flag = 'Create'
            self.flagForReturn = None
            self.update()
        elif self.flagForReturn == 'Turn':
            self.convertForTurn(self.lastParamFirst, self.lastParamSecond, 0-self.lastParamThird)
            self.flag = 'Create'
            self.flagForReturn = None
            self.update()
        else:
            QMessageBox.about(self, "Ошибка", "Последнего действия не найдено")


    def converForMove(self, dx, dy):
        for i in range(len(self.xCircle)):
            self.xCircle[i] += dx
            self.yCircle[i] += dy
        for i in range(len(self.xGip)):
            self.xGip[i] += dx
            self.yGip[i] += dy

    def inputDataForMove(self):
        try:
            dx = float(self.lineEdit_5.text())
            dy = float(self.lineEdit_6.text())
            '''
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            '''
            self.converForMove(dx, dy)
            
            self.lastParamFirst = dx
            self.lastParamSecond = dy
            self.flagForReturn = 'Move'

            return 1
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильные данные")
            return 0

    def converForMashtab(self, kx, ky, xM, yM):
        for i in range(len(self.xCircle)):
            self.xCircle[i] = kx * self.xCircle[i] + (1 - kx) * xM
            self.yCircle[i] = ky * self.yCircle[i] + (1 - ky) * yM
        for i in range(len(self.xGip)):
            self.xGip[i] = kx * self.xGip[i] + (1 - kx) * xM
            self.yGip[i] = ky * self.yGip[i] + (1 - ky) * yM

    def inputDataForMashtab(self):
        try:
            kx = float(self.lineEdit_7.text())
            ky = float(self.lineEdit_8.text())
            xM = float(self.lineEdit_9.text())
            yM = float(self.lineEdit_10.text())
            if kx == 0 or ky == 0:
                QMessageBox.about(self, "Ошибка", "Вы ввели неправильные коэффициенты")
                return 0
            else:
                self.converForMashtab(kx, ky, xM, yM)

                self.lastParamFirst = kx
                self.lastParamSecond = ky
                self.lastParamThird = xM
                self.lastParamFourth = yM
                self.flagForReturn = 'Mashtab'

                return 1
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильные данные")
            return 0

    def convertForTurn(self, xc, yc, angle):
        for i in range(len(self.xCircle)):
            x = self.xCircle[i]
            y = self.yCircle[i]
            self.xCircle[i] = xc + (x - xc) * cos(radians(angle)) + (y - yc) * sin(radians(angle))
            self.yCircle[i] = yc - (x - xc) * sin(radians(angle)) + (y - yc) * cos(radians(angle))
        for i in range(len(self.xGip)):
            x = self.xGip[i]
            y = self.yGip[i]
            self.xGip[i] = xc + (x - xc) * cos(radians(angle)) + (y - yc) * sin(radians(angle))
            self.yGip[i] = yc - (x - xc) * sin(radians(angle)) + (y - yc) * cos(radians(angle))

    def inputDataForTurn(self):
        try:
            xc = float(self.lineEdit_11.text())
            yc = float(self.lineEdit_13.text())
            angle = float(self.lineEdit_14.text())
            '''
            self.lineEdit_11.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
            '''
            angle = 0 - angle
            self.convertForTurn(xc, yc, angle)

            self.lastParamFirst = xc
            self.lastParamSecond = yc
            self.lastParamThird = angle
            self.flagForReturn = 'Turn'
            return 1
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильные данные")
            return 0
    
    def turnPic(self):
        if self.inputDataForTurn():
            self.flag = 'Create'
            self.update()


    def mashtabPic(self):
        if self.inputDataForMashtab():
            self.flag = 'Create'
            self.update()

    def movePic(self):
        if self.inputDataForMove():
            self.flag = 'Create'
            self.update()

    def createPic(self):
        if self.a != None:
            self.flag = 'Create'
            self.xCircle, self.yCircle, self.xGip, self.yGip = createMass(self.a, self.b, self.c, self.r)
            if self.xCircle == [] or self.xGip == []:
                QMessageBox.about(self, "Ошибка", "Пересечения не найдено")
            else:
                self.xCircle, self.yCircle, self.xGip, self.yGip = findMashtab(self.xCircle, self.yCircle, self.xGip, self.yGip, self.a, self.b)
                self.moveX, self.moveY = findMoves(self.xCircle, self.yCircle)
            self.update()
        else:
            QMessageBox.about(self, "Ошибка", "Вы не ввели данные")

    def fillNotUsed(self):
        brush = QBrush(Qt.white)
        self.painter.setPen(QPen(Qt.white, 1))
        self.painter.setBrush(brush)
        self.painter.drawRect(0,0,10,627)
        self.painter.drawRect(0, 471, 857, 627)
        self.painter.drawRect(0, 0, 857, 10)
        self.painter.drawRect(741, 1, 857, 627)

    def drawFunc(self):
        self.painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        self.painter.drawLine(self.X[0], self.X[1], self.X[2], self.X[3])
        self.painter.drawLine(self.Y[0], self.Y[1], self.Y[2], self.Y[3])
        points = QPolygon([QPoint(self.X[0], self.X[1]), QPoint(self.X[0] - 10, self.X[1] + 20), QPoint(self.X[0] + 10, self.X[1] + 20)])
        self.painter.drawPolygon(points)
        points = QPolygon([QPoint(self.Y[2], self.Y[3]), QPoint(self.Y[2] - 20, self.Y[3] - 10), QPoint(self.Y[2] - 20, self.Y[3] + 10)])
        self.painter.drawPolygon(points)
        point = []
        for i in range(len(self.xCircle)):
            point.append(QPoint(10 + self.xCircle[i] + self.moveX, 481 - (10 + self.yCircle[i] + self.moveY)))
        for i in range(len(self.xGip)):
            point.append(QPoint(10 + self.xGip[i] + self.moveX, 481 - (10 + self.yGip[i] + self.moveY)))
        points = QPolygon([i for i in point])
        self.painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        self.painter.setBrush(QBrush(Qt.gray, Qt.BDiagPattern))
        self.painter.drawPolygon(points)

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black, 3))
        self.painter.drawRect(10,10,731,461)
        self.painter.setPen(QPen(Qt.black, 2))
        if self.flag == 'Create':
            self.painter.setPen(QPen(Qt.black, 3))
            self.drawFunc()
            self.flag = None
        self.fillNotUsed()
        self.painter.end()
        self.flag = None

    def clickBtnAdd(self):
        try:
            a = float(self.lineEdit.text())
            b = float(self.lineEdit_2.text())
            r = float(self.lineEdit_3.text())
            c = float(self.lineEdit_4.text())
            if r <= 0:
                QMessageBox.about(self, "Ошибка", "Вы ввели неправильный радиус")
            elif c <= 0:
                QMessageBox.about(self, "Ошибка", "Вы ввели неправильный коэффициент c")
            else:
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                self.lineEdit_3.setText('')
                self.lineEdit_4.setText('')

                self.listWidget.clear()
                self.listWidget.addItem('a = ' + str(a))
                self.listWidget.addItem('b = ' + str(b))
                self.listWidget.addItem('r = ' + str(r))
                self.listWidget.addItem('c = ' + str(c))

                self.a = a
                self.b = b
                self.r = r
                self.c = c
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильные данные")

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()