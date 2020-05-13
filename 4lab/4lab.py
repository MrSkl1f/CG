import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets  
from PyQt5.QtGui import QPen, QColor 
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtCore import Qt
from math import *
import time
from math import *
import numpy as np

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.canonEquation.setChecked(1)
        self.radio = 1

        self.centerX = 1121 / 2
        self.centerY = 671 / 2

        self.scene = QtWidgets.QGraphicsScene(0, 0, 1121, 671)
        self.graphicsView.setScene(self.scene)
        self.scene.setBackgroundBrush(Qt.white)
        self.pen = QPen()
        self.pen.setWidth(1)
        self.pen.setColor(Qt.black)
        
        self.blackScene.clicked.connect(self.blackSceneChange)
        self.whiteScene.clicked.connect(self.whiteSceneChange)
        self.redScene.clicked.connect(self.redSceneChange)
        self.blueScene.clicked.connect(self.blueSceneChange)

        self.blackLine.clicked.connect(self.blackLineChange)
        self.whiteLine.clicked.connect(self.whiteLineChange)
        self.redLine.clicked.connect(self.redLineChange)
        self.blueLine.clicked.connect(self.blueLineChange)

        self.drawCircle.clicked.connect(self.circleManager)
        self.drawEllipse.clicked.connect(self.ellipseManager)

        self.clearScene.clicked.connect(self.clearSceneManager)

        self.changePenWidth.clicked.connect(self.changeWidth)

        self.drawCircleSpector.clicked.connect(self.multipleCircles)
        self.drawEllipseSpector.clicked.connect(self.multipleEllipse)

    def clearSceneManager(self):
        self.scene.clear()

    def changeWidth(self):
        try:
            width = int(self.penWidth.text())
        except:
            pass
        finally:
            self.pen.setWidth(width)

    def radioManager(self):
        if self.canonEquation.isChecked():
            self.radio = 1
        elif self.paramEquation.isChecked():
            self.radio = 2
        elif self.methodBrezenhem.isChecked():
            self.radio = 3
        elif self.methodMidpoint.isChecked():
            self.radio = 4
        else:
            self.radio = 5

    def blackSceneChange(self):
        self.scene.setBackgroundBrush(Qt.black)
    def whiteSceneChange(self):
        self.scene.setBackgroundBrush(Qt.white)
    def redSceneChange(self):
        self.scene.setBackgroundBrush(Qt.red)
    def blueSceneChange(self):
        self.scene.setBackgroundBrush(Qt.blue)

    def blackLineChange(self):
        self.pen.setColor(Qt.black)
    def whiteLineChange(self):
        self.pen.setColor(Qt.white)
    def redLineChange(self):
        self.pen.setColor(Qt.red)
    def blueLineChange(self):
        self.pen.setColor(Qt.blue)

    def drawPointCanon(self, cx, cy, x, y):
        self.scene.addLine(cx + x + self.centerX, cy + y + self.centerY, cx + x + self.centerX, cy + y + self.centerY, self.pen)

    def drawPointParam(self, cx, cy, x, y):
        self.scene.addLine(cx + x + self.centerX, cy + y + self.centerY, cx + x + self.centerX, cy + y + self.centerY, self.pen)

    def drawPointBrez(self, cx, cy, x, y):
        self.scene.addLine(cx + x + self.centerX, cy + y + self.centerY, cx + x + self.centerX, cy + y + self.centerY, self.pen)

    def drawPointMidPoint(self, cx, cy, x, y):
        self.scene.addLine(cx + x + self.centerX, cy + y + self.centerY, cx + x + self.centerX, cy + y + self.centerY, self.pen)

    def circleCanon(self, centerX, centerY, radius):
        i = 0
        while i < radius + 1:
            y = round(sqrt(radius ** 2 - i ** 2))
            # по окнанам
            self.drawPointCanon(centerX, centerY, i, y)
            self.drawPointCanon(centerX, centerY, i, -y)
            self.drawPointCanon(centerX, centerY, -i, y)
            self.drawPointCanon(centerX, centerY, -i, -y)
            i += 1
        i = 0
        while i < radius + 1:
            x = round(sqrt(radius ** 2 - i ** 2))
            self.drawPointCanon(centerX, centerY, x, i)
            self.drawPointCanon(centerX, centerY, x, -i)
            self.drawPointCanon(centerX, centerY, -x, i)
            self.drawPointCanon(centerX, centerY, -x, -i)
            i += 1

    def circleParam(self, centerX, centerY, radius):
        length = round(pi * radius / 2 )  # длина четврети окружности
        i = 0
        while i < length + 1:
            x = round(radius * cos(i / radius))
            y = round(radius * sin(i / radius))
            self.drawPointParam(centerX, centerY, x, y)
            self.drawPointParam(centerX, centerY, x, -y)
            self.drawPointParam(centerX, centerY, -x, y)
            self.drawPointParam(centerX, centerY, -x, -y)
            i += 1

    def circleBrez(self, centerX, centerY, radius):
        x = 0   # задание начальных значений
        y = radius
        deltaI = 2 * (1 - radius)   # значение deltaI(x,y)  при (0,R)
        while y >= 0:
            # высвечивание текущего пиксела
            self.drawPointParam(centerX, centerY, x, y)
            self.drawPointParam(centerX, centerY, x, -y)
            self.drawPointParam(centerX, centerY, -x, y)
            self.drawPointParam(centerX, centerY, -x, -y)

            if deltaI < 0:  # пиксель лежит внутри окружности
                buf = 2 * (deltaI + y) - 1
                x += 1

                if buf <= 0:  # горизонтальный шаг
                    deltaI = deltaI + 2 * x + 1
                else:  # диагональный шаг
                    y -= 1
                    deltaI = deltaI + 2 * (x - y + 1)

                continue

            if deltaI > 0:  # пиксель лежит вне окружности
                buf = 2 * (deltaI - x) - 1
                y -= 1

                if buf > 0:  # вертикальный шаг
                    deltaI = deltaI - 2 * y + 1
                else:  # диагональный шаг
                    x += 1
                    deltaI = deltaI + 2 * (x - y + 1)

                continue

            if deltaI == 0.0:  # пиксель лежит на окружности
                x += 1   # диагональный шаг
                y -= 1
                deltaI = deltaI + 2 * (x - y + 1)

    def circleMidPoint(self, centerX, centerY, radius):
        x = 0  # начальные значения
        y = radius
        p = 5 / 4 - radius  # (x + 1)^2 + (y - 1/2)^2 - r^2
        while x <= y:
            self.drawPointMidPoint(centerX, centerY, x, y)
            self.drawPointMidPoint(centerX, centerY, x, -y)
            self.drawPointMidPoint(centerX, centerY, -x, y)
            self.drawPointMidPoint(centerX, centerY, -x, -y)

            self.drawPointMidPoint(centerX, centerY, y, x)
            self.drawPointMidPoint(centerX, centerY, y, -x)
            self.drawPointMidPoint(centerX, centerY, -y, x)
            self.drawPointMidPoint(centerX, centerY, -y, -x)

            x += 1

            if p < 0: 
                p += 2 * x + 1
            else:   
                p += 2 * (x - y) + 5
                y -= 1
    
    def circleLibrary(self, centerX, centerY, radius):
        self.scene.addEllipse(centerX - radius + self.centerX, centerY - radius + self.centerY, radius * 2, radius * 2, self.pen)

    def circleManager(self):
        try:
            centerX = float(self.xCenterCircle.text())
            centerY = float(self.yCenterCircle.text())
            radius = float(self.radiusCircle.text())
        except:
            pass
        finally:
            self.radioManager()
            if self.radio == 1:
                self.circleCanon(centerX, centerY, radius)
            elif self.radio == 2:
                self.circleParam(centerX, centerY, radius)
            elif self.radio == 3:
                self.circleBrez(centerX, centerY, radius)
            elif self.radio == 4:
                self.circleMidPoint(centerX, centerY, radius)
            else:
                self.circleLibrary(centerX, centerY, radius)

    def drawPointEllipse(self, cx, cy, x, y):
        self.scene.addLine(cx + x + self.centerX, cy + y + self.centerY, cx + x + self.centerX, cy + y + self.centerY, self.pen)

    def ellipseCanon(self, coefA, coefB, centerX, centerY):
        i = 0
        while i < coefA + 1:
            y = round(coefB * sqrt(1.0 - i ** 2 / coefA / coefA))
            self.drawPointEllipse(centerX, centerY, i, y)
            self.drawPointEllipse(centerX, centerY, i, -y)
            self.drawPointEllipse(centerX, centerY, -i, y)
            self.drawPointEllipse(centerX, centerY, -i, -y)
            i += 1
        i = 0
        while i < coefB + 1:
            x = round(coefA * sqrt(1.0 - i ** 2 / coefB / coefB))
            self.drawPointEllipse(centerX, centerY, x, i)
            self.drawPointEllipse(centerX, centerY, x, -i)
            self.drawPointEllipse(centerX, centerY, -x, i)
            self.drawPointEllipse(centerX, centerY, -x, -i)
            i += 1

    def ellipseParam(self, coefA, coefB, centerX, centerY):
        m = max(coefA, coefB)
        l = round(pi * m / 2)
        i = 0
        while i < l + 1:
            x = round(coefA * cos(i / m))
            y = round(coefB * sin(i / m))
            self.drawPointEllipse(centerX, centerY, x, y)
            self.drawPointEllipse(centerX, centerY, x, -y)
            self.drawPointEllipse(centerX, centerY, -x, y)
            self.drawPointEllipse(centerX, centerY, -x, -y)
            i += 1
            
    def ellipseBrez(self, coefA, coefB, centerX, centerY):
        x = 0  # начальные значения
        y = coefB
        coefA = coefA ** 2
        deltaI = round(coefB * coefB / 2 - coefA * coefB * 2 + coefA / 2)
        coefB = coefB ** 2
        sumCoefs = coefA + coefB
        while y >= 0:
            self.drawPointEllipse(centerX, centerY, x, y)
            self.drawPointEllipse(centerX, centerY, x, -y)
            self.drawPointEllipse(centerX, centerY, -x, y)
            self.drawPointEllipse(centerX, centerY, -x, -y)
            if deltaI < 0:  # пиксель лежит внутри эллипса
                buf = 2 * (deltaI + coefA * y) - coefA
                x += 1
                if buf <= 0:  # горизотальный шаг
                    deltaI = deltaI + 2 * coefB * x + coefB
                else:  # диагональный шаг
                    y -= 1
                    deltaI = deltaI + 2 * (coefB * x - coefA * y) + sumCoefs

                continue

            if deltaI > 0:  # пиксель лежит вне эллипса
                buf = 2 * (deltaI - coefB * x) - coefB
                y -= 1

                if buf > 0:  # вертикальный шаг
                    deltaI = deltaI - 2 * y * coefA + coefA
                else:  # диагональный шаг
                    x += 1
                    deltaI = deltaI + 2 * (x * coefB - y * coefA) + sumCoefs

                continue

            if deltaI == 0.0:  # пиксель лежит на окружности
                x += 1  # диагональный шаг
                y -= 1
                deltaI = deltaI + 2 * (x * coefB - y * coefA) + sumCoefs

    
    def ellipseMiddle(self, coefA, coefB, centerX, centerY):
        x = 0   # начальные положения
        a2 = coefA ** 2
        b2 = coefB ** 2
        y = coefB
        p = b2 - a2 * coefB + 0.25 * a2   # начальное значение параметра принятия решения в области tg<1
    
        while (b2) * x < (a2) * y:  # пока тангенс угла наклона меньше 1
            self.drawPointEllipse(centerX, centerY, x, y)
            self.drawPointEllipse(centerX, centerY, x, -y)
            self.drawPointEllipse(centerX, centerY, -x, y)
            self.drawPointEllipse(centerX, centerY, -x, -y)

            x += 1

            if p < 0:  # средняя точка внутри эллипса, ближе верхний пиксел, горизонтальный шаг
                p += 2 * (b2) * x + (b2)
            else:   # средняя точка вне эллипса, ближе диагональный пиксел, диагональный шаг
                y -= 1
                p += 2 * (b2) * x - 2 * (a2) * y + (b2)

        p = (b2) * ((x + 0.5) ** 2) + (a2) * ((y - 1) ** 2) - (a2) * (b2)
        # начальное значение параметра принятия решения в области tg>1 в точке (х + 0.5, y - 1) полседнего положения
        
        while y >= 0:
            self.drawPointEllipse(centerX, centerY, x, y)
            self.drawPointEllipse(centerX, centerY, x, -y)
            self.drawPointEllipse(centerX, centerY, -x, y)
            self.drawPointEllipse(centerX, centerY, -x, -y)

            y -= 1

            if p > 0:
                p -= 2 * (a2) * y + (a2)
            else:
                x += 1
                p += 2 * ((b2) * x - (a2) * y) + (a2)

    def drawEllipseLibrary(self, a, b, x, y):
        self.scene.addEllipse(x - a + self.centerX, y - b + self.centerY, a * 2, b * 2, self.pen)

    def ellipseManager(self):
        try:
            centerX = float(self.xCenterEllipse.text())
            centerY = float(self.yCenterEllipse.text())
            coefA = float(self.coefA.text())
            coefB = float(self.coefB.text())
        except:
            pass
        finally:
            self.radioManager()
            if self.radio == 1:
                self.ellipseCanon(coefA, coefB, centerX, centerY)
            elif self.radio == 2:
                self.ellipseParam(coefA, coefB, centerX, centerY)
            elif self.radio == 3:
                self.ellipseBrez(coefA, coefB, centerX, centerY)
            elif self.radio == 4:
                self.ellipseMiddle(coefA, coefB, centerX, centerY)
            else:
                self.drawEllipseLibrary(coefA, coefB, centerX, centerY)

    def multipleCircles(self):
        try:
            step = int(self.stepSpektor.text())
            count = int(self.countCircles.text())
        except:
            pass
        finally:
            self.radioManager()
            for i in range(step, step * count + step, step):
                if self.radio == 1:
                    self.circleCanon(0, 0, i)
                elif self.radio == 2:
                    self.circleParam(0, 0, i)
                elif self.radio == 3:
                    self.circleBrez(0, 0, i)
                elif self.radio == 4:
                    self.circleMidPoint(0, 0, i)
                else:
                    self.circleLibrary(0, 0, i)

    def multipleEllipse(self):
        try:
            step = int(self.stepSpektor.text())
            count = int(self.countCircles.text())
        except:
            pass
        finally:
            self.radioManager()
            for i in range(step, step * count + step, step):
                if self.radio == 1:
                    self.ellipseCanon(i, i * 2, 0, 0)
                elif self.radio == 2:
                    self.ellipseParam(i, i * 2, 0, 0)
                elif self.radio == 3:
                    self.ellipseBrez(i, i * 2, 0, 0)
                elif self.radio == 4:
                    self.ellipseMiddle(i, i * 2, 0, 0)
                else:
                    self.drawEllipseLibrary(i, i * 2, 0, 0)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()