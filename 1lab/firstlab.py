import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore import Qt, QPointF
from math import *
import time


def findCircles(frstArr, tmp):
    for i in range(len(frstArr[0])):
        for j in range(i + 1, len(frstArr[0]) ):
            for k in range(j + 1, len(frstArr[0])):
                if (frstArr[1][j] - frstArr[1][i]) * (frstArr[0][k] - frstArr[0][i]) == (frstArr[1][k] - frstArr[1][i]) * (frstArr[0][j] - frstArr[0][i]):
                    pass
                else:
                    
                    A = frstArr[0][j] - frstArr[0][i]; C = frstArr[0][k] - frstArr[0][i]
                    B = frstArr[1][j] - frstArr[1][i]; D = frstArr[1][k] - frstArr[1][i]
                    E = A * (frstArr[0][j] + frstArr[0][i]) + B * (frstArr[1][j] + frstArr[1][i])
                    F = C * (frstArr[0][k] + frstArr[0][i]) + D * (frstArr[1][k] + frstArr[1][i])
                    G = 2 * (A * (frstArr[1][k] - frstArr[1][j]) - B * (frstArr[0][k] - frstArr[0][j]))
                    xCenter = (D * E - B * F) / G
                    yCenter = (A * F - C * E) / G
                    R = sqrt((frstArr[0][i] - xCenter) ** 2 + (frstArr[1][i] - yCenter) ** 2)
                    if xCenter < 1e-5 and xCenter > -1e-5:
                        xCenter = 0.0
                    if yCenter < 1e-5 and yCenter > -1e-5:
                        yCenter = 0.0
                    tmp[0].append(round(xCenter, 3))
                    tmp[1].append(round(yCenter, 3))
                    tmp[2].append(round(R, 3))
                    
                    '''
                    x1 = frstArr[0][i]; x2 = frstArr[0][j]; x3 = frstArr[0][k]
                    y1 = frstArr[1][i]; y2 = frstArr[1][j]; y3 = frstArr[1][k]
                    if x2 - x1 != 0 and x3 - x2 != 0:
                        Ma=(y2 - y1) / (x2 - x1)
                        Mb=(y3 - y2) / (x3 - x2)
                        if Ma - Mb != 0 and Ma != 0 and Mb != 0:
                            xCenter=(Ma * Mb * (y1 - y3) + Mb * (x1 + x2) - Ma * (x2 + x3)) / (2 * (Mb - Ma))
                            yCenter=-1 / Ma * (xCenter - (x1 + x2) / 2) + ((y1 + y2) / 2)
                            R = sqrt((frstArr[0][i] - xCenter) ** 2 + (frstArr[1][i] - yCenter) ** 2)
                            
                            if xCenter < 1e-5 and xCenter > -1e-5:
                                xCenter = 0.0
                            if yCenter < 1e-5 and yCenter > -1e-5:
                                yCenter = 0.0

                            tmp[0].append(xCenter)
                            tmp[1].append(yCenter)
                            tmp[2].append(R)
                    else:
                        pass
                    '''
    return tmp

def deleteRepeatedCircles(resultArr):
    length = len(resultArr)
    index = []
    for i in range(length - 1):
        if resultArr[i] == resultArr[i + 1]:
            index.append(resultArr[i + 1])
            length -= 1
    for i in range(len(index)):
        resultArr.remove(index[i])
    return resultArr

def findSuitableCircles(tmp, resultArr):
    countOfCircles = len(tmp[0])
    for i in range(countOfCircles):
        for j in range(i + 1, countOfCircles):
            if tmp[0][i] + tmp[2][i] == tmp[0][j] - tmp[2][j] and tmp[1][i] != tmp[1][j]:
                resultArr.append([[tmp[0][i], tmp[1][i], tmp[2][i]], [tmp[0][j], tmp[1][j], tmp[2][j]]])    
            if tmp[0][i] - tmp[2][i] == tmp[0][j] + tmp[2][j] and tmp[1][i] != tmp[1][j]:
                resultArr.append([[tmp[0][j], tmp[1][j], tmp[2][j]], [tmp[0][i], tmp[1][i], tmp[2][i]]])
    return resultArr

def createCircles(frstArr, scndArr):
    tmp = [[], [], []]
    tmp = findCircles(frstArr, tmp)
    tmp = findCircles(scndArr, tmp)
    resultArr = []
    resultArr = findSuitableCircles(tmp, resultArr)
    deleteRepeatedCircles(resultArr)
    return resultArr

def findUppersLowers(tmp):
    if tmp[0][0] > tmp[1][0]:
        UpperX = tmp[0][0] + tmp[0][2]
        LowerX = tmp[1][0] - tmp[1][2]
    else:
        UpperX = tmp[1][0] + tmp[1][2]
        LowerX = tmp[0][0] - tmp[0][2]

    if tmp[0][1] > tmp[1][1]:
        UpperY = tmp[0][1] + tmp[0][2]
        LowerY = tmp[1][1] - tmp[1][2]
    else:
        UpperY = tmp[1][1] + tmp[1][2]
        LowerY = tmp[0][1] - tmp[0][2]
    return UpperX, UpperY, LowerX, LowerY

def findMoves(tmp):
    UpperX, UpperY, LowerX, LowerY = findUppersLowers(tmp)
    centerX = (UpperX + LowerX) / 2
    centerY = (UpperY + LowerY) / 2
    moveX = (721 / 2 - centerX)
    moveY = (511 / 2 - centerY)
    return moveX, moveY

def mashtabCheck(tmp, mashtab):
    UpperX, UpperY, LowerX, LowerY = findUppersLowers(tmp)
    coefX = floor(float(721 - 2 * 18) / float(UpperX - LowerX))
    coefY = floor(float(511 - 2 * 18) / float(UpperY - LowerY))
    if coefX > coefY:
        mashtab = coefY
    else:
        mashtab = coefX
    return mashtab

def resultLines(forLines, tmp):
    if tmp[0][0] + tmp[0][2] == tmp[1][0] - tmp[1][2]:
        forLines.append([tmp[0][0] + tmp[0][2], tmp[0][1]])
        forLines.append([tmp[1][0] - tmp[1][2], tmp[1][1]])
    else:
        forLines.append([tmp[0][0] - tmp[0][2], tmp[0][1]])
        forLines.append([tmp[1][0] + tmp[1][2], tmp[1][1]])
    return forLines

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.clickBtnFrst)
        self.pushButton_2.clicked.connect(self.clickBtnScnd)
        self.pushButton_3.clicked.connect(self.clearListFrst)
        self.pushButton_4.clicked.connect(self.clearListScnd)
        self.pushButton_5.clicked.connect(self.clickBtnCreating)
        self.pushButton_6.clicked.connect(self.goOnClick)
        self.pushButton_7.clicked.connect(self.clickBtnDeleteFrst)
        self.pushButton_8.clicked.connect(self.clickBtnDeleteScnd)
        self.mashtab = 20
        self.point = None
        self.cur = 0
        self.check = 0
        self.moveX = 0
        self.moveY = 0
        self.frstArr = [[], []]
        self.scndArr = [[], []]
        self.result = []
        self.currentPic = 0
        self.allPics = 0
        self.tmp = []
        self.lengthFrst = 0
        self.lengthScnd = 0

    def clickBtnFrst(self):
        XFirst = self.lineEdit.text()
        YFirst = self.lineEdit_2.text()
        try:
            XFirst = float(XFirst)
            YFirst = float(YFirst)
            self.lengthFrst += 1
            self.listWidget.addItem('%d. ' % self.lengthFrst + '(' + str(XFirst) + ';' + str(YFirst) + ')') 
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.frstArr[0].append(XFirst)
            self.frstArr[1].append(YFirst)
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильные значения")

    def clickBtnDeleteFrst(self):
        index = self.lineEdit_5.text()
        try:
            index = int(index) - 1
            if index >= 0 and index < self.lengthFrst:
                del self.frstArr[0][index]
                del self.frstArr[1][index]
                self.listWidget.clear()
                self.lineEdit_5.setText('')
                self.lengthFrst -= 1
                for i in range(len(self.frstArr[0])):
                    self.listWidget.addItem('%d. ' % (i + 1) + '(' + str(self.frstArr[0][i]) + ';' + str(self.frstArr[1][i]) + ')')
            else:
                if index < 0:
                    QMessageBox.about(self, "Ошибка", "Число должно быть больше нуля")
                else:
                    QMessageBox.about(self, "Ошибка", "Число должно быть меньшего общего количества")
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильное значение")

    def clickBtnScnd(self):
        XSecond = self.lineEdit_3.text()
        YSecond = self.lineEdit_4.text()
        try:
            XSecond = float(XSecond)
            YSecond = float(YSecond)
            self.lengthScnd += 1
            self.listWidget_2.addItem('%d. ' % self.lengthScnd + '(' + str(XSecond) + ';' + str(YSecond) + ')') 
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.scndArr[0].append(XSecond)
            self.scndArr[1].append(YSecond)
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильные значения")

    def clickBtnDeleteScnd(self):
        index = self.lineEdit_6.text()
        try:
            index = int(index) - 1
            if index >= 0 and index < self.lengthScnd:
                del self.scndArr[0][index]
                del self.scndArr[1][index]
                self.listWidget_2.clear()
                self.lineEdit_6.setText('')
                self.lengthScnd -= 1
                for i in range(len(self.scndArr[0])):
                    self.listWidget_2.addItem('%d. ' % (i + 1) + '(' + str(self.scndArr[0][i]) + ';' + str(self.scndArr[1][i]) + ')')
            else:
                if index < 0:
                    QMessageBox.about(self, "Ошибка", "Число должно быть больше нуля")
                else:
                    QMessageBox.about(self, "Ошибка", "Число должно быть меньшего общего количества")
        except:
            QMessageBox.about(self, "Ошибка", "Вы ввели неправильное значение")

    def clearListFrst(self):
        self.listWidget.clear()
        self.frstArr = [[], []]

    def clearListScnd(self):
        self.listWidget_2.clear()
        self.scndArr = [[], []]

    def clickBtnCreating(self):
        if len(self.frstArr[0]) < 3:
            QMessageBox.about(self, "Ошибка", "Не достаточно элементов первого массива")
        elif len(self.scndArr[0]) < 3:
            QMessageBox.about(self, "Ошибка", "Не достаточно элементов второго массива")
        else:
            self.result = createCircles(self.frstArr, self.scndArr)
            self.allPics = len(self.result)
            if self.allPics > 0:
                print(self.result)
                self.currentPic = 1
                self.tmp = self.result[self.currentPic - 1]
                self.tmp = self.result[self.currentPic - 1]
                self.listWidget_3.clear()
                self.listWidget_3.addItem('1/' + str(self.allPics)) 
                self.point = 'Yes'
                self.check = len(self.result)
                self.update()
            else:
                QMessageBox.about(self, "Ошибка", "Подходящих окружностей не найдено")
    
    def goOnClick(self):
        if self.allPics == 0:
            QMessageBox.about(self, "Ошибка", "Вы не построили окружности")
        elif self.currentPic == self.allPics:
            QMessageBox.about(self, "Ошибка", "вы пролистали все окружности")
        else:
            self.listWidget_3.clear()
            self.currentPic += 1
            self.tmp = self.result[self.currentPic - 1]
            self.listWidget_3.clear()
            self.listWidget_3.addItem(str(self.currentPic) + '/' + str(self.allPics))
            self.point = 'Yes'
            self.update()

    def printLines(self, arr, i):
        self.painter.drawPoint(arr[0][i] * self.mashtab + self.moveX, 511 - (arr[1][i] * self.mashtab + self.moveY))
        self.painter.drawText(arr[0][i] * self.mashtab + self.moveX, 511 - (arr[1][i] * self.mashtab + self.moveY), \
            '(' + '%.1f' % arr[0][i] + ';' + '%.1f' % arr[1][i] + ')')

    def drawLines(self):
        self.painter.setPen(QPen(Qt.red, 5))
        for i in range(len(self.frstArr[0])):
            if (((self.frstArr[0][i] * self.mashtab - self.tmp[0][0]) ** 2 + (self.frstArr[1][i] * self.mashtab - self.tmp[0][1]) ** 2) == self.tmp[0][2] ** 2):
                self.printLines(self.frstArr, i)
            if (((self.frstArr[0][i] * self.mashtab - self.tmp[1][0]) ** 2 + (self.frstArr[1][i] * self.mashtab - self.tmp[1][1]) ** 2) == self.tmp[1][2] ** 2):
                self.printLines(self.frstArr, i)
        for i in range(len(self.scndArr[0])):
            if (((self.scndArr[0][i] * self.mashtab - self.tmp[0][0]) ** 2 + (self.scndArr[1][i] * self.mashtab - self.tmp[0][1]) ** 2) == self.tmp[0][2] ** 2):
                self.printLines(self.scndArr, i)
            if (((self.scndArr[0][i] * self.mashtab - self.tmp[1][0]) ** 2 + (self.scndArr[1][i] * self.mashtab - self.tmp[1][1]) ** 2) == self.tmp[1][2] ** 2):
                self.printLines(self.scndArr, i)

    def outputResult(self):
        self.listWidget_4.clear()
        self.listWidget_4.addItem('Было построено %d окружностей.' % self.allPics + 'На данной картине мы видим окружности: (%.1f;' % self.tmp[0][0] \
            + '%.1f) ' % self.tmp[0][1] + 'с радиусом %.1f ' % self.tmp[0][2] + \
            '\nи (%.1f;' % self.tmp[1][0] + '%.1f) ' % self.tmp[1][1] + 'с радиусом %.1f.' % self.tmp[1][2] \
            + ' Их внутренняя касательная паралельна оси ординат.')

    def paintEvent(self, event):
        if self.point == 'Yes':
            self.painter = QPainter(self)
            self.painter.setPen(QPen(Qt.black, 2))
            self.outputResult()
            self.mashtab = mashtabCheck(self.tmp, self.mashtab)
            for i in range(2):
                self.tmp[i][0] = self.tmp[i][0] * self.mashtab
                self.tmp[i][1] = self.tmp[i][1] * self.mashtab
                self.tmp[i][2] = self.tmp[i][2] * self.mashtab
            
            forLines = []
            forLines = resultLines(forLines, self.tmp)

            self.moveX, self.moveY = findMoves(self.tmp)
            
            self.painter.setPen(QPen(Qt.black, 3))
            self.painter.drawEllipse((self.tmp[0][0] - self.tmp[0][2]) + self.moveX, 
            511 - ((self.tmp[0][1] + self.tmp[0][2]) + self.moveY),
            2 * self.tmp[0][2], 2 * self.tmp[0][2])

            self.painter.setPen(QPen(Qt.black, 3))
            self.painter.drawEllipse((self.tmp[1][0] - self.tmp[1][2]) + self.moveX, 
            511 - ((self.tmp[1][1] + self.tmp[1][2]) + self.moveY), 
            2 * self.tmp[1][2], 2 * self.tmp[1][2])
            
            self.painter.setPen(QPen(Qt.gray, 3))
            self.painter.drawLine(forLines[0][0] + self.moveX, 511 - (forLines[0][1] + self.moveY),
            forLines[1][0] + self.moveX, 511 - (forLines[1][1] + self.moveY))

            self.drawLines()

            self.mashtab = 20
            self.painter.end()
            self.point = None
        
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black, 3))
        self.painter.drawRect(10,10,731,521)
        self.painter.setPen(QPen(Qt.gray, 1))
        self.painter.drawLine(150, 10, 150, 210)
        self.painter.drawLine(10, 115, 301, 115)
        self.painter.end()


    def returnArrs(self):
        return self.frstArr, self.scndArr

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()