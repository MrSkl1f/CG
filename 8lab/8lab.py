import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtCore
from math import sqrt
import design

def sign(x):
    if not x:
        return 0
    return x / abs(x)

class CutterApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scene = myScene(10, 10, 871, 541)
        self.graphicsView.setScene(self.scene)
        self.scene.setBackgroundBrush(QtCore.Qt.white)

        self.pushButton.clicked.connect(self.setBars)
        self.pushButton_2.clicked.connect(self.setLines)
        self.pushButton_3.clicked.connect(self.cutScene)
        self.pushButton_4.clicked.connect(self.clearScene)
        
        self.pen = QtGui.QPen()
        self.pen.setWidth(1)
        self.pen.setColor(QtCore.Qt.black)
        self.pen.setWidth(2)
        
        self.inputBars = False
        self.inputPolygon = False
        
        self.lines = []
        self.lastPoint = None
        
        self.colorInRect = QtCore.Qt.red
        self.colorOutRect = QtCore.Qt.blue
        
        self.polygon = []
        self.lastEdge = None

    def clearScene(self):
        self.scene.clear()
        self.listWidget.clear()
        
        self.inputBars = False
        self.inputPolygon = False
        
        self.lines = []
        self.lastPoint = None
        
        self.polygon = []
        self.lastEdge = None
        
    def setBars(self):
        if self.inputBars:
            self.inputBars = False
            self.pushButton_2.setDisabled(False)
            self.pushButton_3.setDisabled(False)
            self.pushButton_4.setDisabled(False)
        else:
            self.inputBars = True
            self.pushButton_2.setDisabled(True)
            self.pushButton_3.setDisabled(True)
            self.pushButton_4.setDisabled(True)

    def setLines(self):
        if self.inputPolygon:
            self.pen.setColor(QtCore.Qt.black)
            self.scene.addLine(self.polygon[len(self.polygon) - 1].x(), self.polygon[len(self.polygon) - 1].y(), self.polygon[0].x(), self.polygon[0].y(), self.pen)
            self.inputPolygon = False
            self.pushButton.setDisabled(False)
            self.pushButton_3.setDisabled(False)
            self.pushButton_4.setDisabled(False)
        else:
            self.inputPolygon = True
            self.pushButton.setDisabled(True)
            self.pushButton_3.setDisabled(True)
            self.pushButton_4.setDisabled(True)

    def addLine(self, point):
        if self.lastPoint == None:
            self.lastPoint = point
        else:
            self.lines.append([[self.lastPoint.x(), self.lastPoint.y()], \
                                            [point.x(), point.y()]])
            x = self.lastPoint.x()
            y = self.lastPoint.y()
            self.listWidget.addItem('( (' + str(x) + ' ; ' + str(y) + ') ; (' + \
                                                    str(point.x()) + ' ; ' + str(point.y()) + ') )')
            self.pen.setColor(self.colorOutRect)
            self.scene.addLine(x, y, point.x(), point.y(), self.pen)
            self.lastPoint = None    

    def addEdge(self, point):
        if self.lastEdge == None:
            self.lastEdge = point
            self.polygon.append(QtCore.QPointF(point.x(), point.y()))
        else:
            self.pen.setColor(QtCore.Qt.black)
            self.polygon.append(QtCore.QPointF(point.x(), point.y()))
            x = self.lastEdge.x()
            y = self.lastEdge.y()
            self.scene.addLine(x, y, point.x(), point.y(), self.pen)
            self.lastEdge = point

    def addPoint(self, point):
        if self.inputBars:
            self.addLine(point)
        else:
            self.addEdge(point)
    
    def drawAllLines(self):
        for i in range(len(self.lines)):
                self.pen.setColor(self.colorOutRect)
                P1 = QtCore.QPointF(self.lines[i][0][0], self.lines[i][0][1])
                P2 = QtCore.QPointF(self.lines[i][1][0], self.lines[i][1][1])
                self.scene.addLine(P1.x(), P1.y(), P2.x(), P2.y(), self.pen)
    
    def isConvex(self):
        points = self.polygon
        
        flag = True
        
        vo = points[0]
        vi = points[1]
        vn = points[2]

        xFirst = vi.x() - vo.x()
        yFirst = vi.y() - vo.y()

        xSecond = vn.x() - vi.x()
        ySecond = vn.y() - vi.y()
        
        signOrdinate = xFirst * ySecond - xSecond * yFirst
        previous = sign(signOrdinate)
        
        for i in range(2, len(points) - 1):
            if not flag:
                break
            vo = points[i - 1]
            vi = points[i]
            vn = points[i + 1]
            
            # векторное произведение двух векторов
            xFirst = vi.x() - vo.x()
            yFirst = vi.y() - vo.y()

            xSecond = vn.x() - vi.x()
            ySecond = vn.y() - vi.y()
            
            signOrdinate = xFirst * ySecond - xSecond * yFirst
            current = sign(signOrdinate)
            if current != previous:
                flag = 0
            previous = current
        
        vo = points[len(points) - 1]
        vi = points[0]
        vn = points[1]
        xFirst = vi.x() - vo.x()
        yFirst = vi.y() - vo.y()

        xSecond = vn.x() - vi.x()
        ySecond = vn.y() - vi.y()
        
        signOrdinate = xFirst * ySecond - xSecond * yFirst
        current = sign(signOrdinate)
        
        if current != previous:
            flag = 0
        
        return flag * current

    def scalar(self, v1, v2):
        return v1.x() * v2.x() + v1.y() * v2.y()
        
    def cutScene(self):
        norm = self.isConvex()
        if not norm:
            QtWidgets.QMessageBox.warning(self, "Ошибка!", "Отсекатель не выпуклый!")
            return
        for line in self.lines:
            self.pen.setColor(QtCore.Qt.red)
            self.CyrusBeck(line, self.polygon, norm)

    def CyrusBeck(self, currentLine, points, norm):
        # инициализируем пределы значений параметра, предполагая, что весь отрезок полностью видимый
        # максимизируем t нижнее и t верхнее, исходя из того что 0 <= t <= 1
        tLower = 0
        tTop = 1

        # вычисляем директрису(определяет направление/ориентацию отрезка) directrix= p1 - p2
        directrix = QtCore.QPointF()
        directrix.setX(currentLine[1][0] - currentLine[0][0])
        directrix.setY(currentLine[1][1] - currentLine[0][1])

        # главный цикл по сторонам отсекателя
        for i in range(len(points)):
            # весовой множитель удаленности гранничной точки от р1(берем граничную точку равной вершине)
            distanceWeight = QtCore.QPointF()
            distanceWeight.setX(currentLine[0][0] - points[i].x())
            distanceWeight.setY(currentLine[0][1] - points[i].y())

            # определяем нормаль
            normal = QtCore.QPointF()
            if i == len(points) - 1:
                normal.setX(-norm * (points[0].y() - points[i].y()))
                normal.setY(norm * (points[0].x() - points[i].x()))
            else:
                normal.setX(-norm * (points[i + 1].y() - points[i].y()))
                normal.setY(norm * (points[i + 1].x() - points[i].x()))
            # определяем скалярные произведения
            Dscalar = self.scalar(directrix, normal)
            Wscalar = self.scalar(distanceWeight, normal)
            if Dscalar == 0:
                # если отрезок параллелен ребру отсекателю
                if Wscalar < 0:
                    # виден ли
                    return
            else:
                
                # отрезок невырожден, определяем t
                t = - Wscalar / Dscalar
                print(t)
                if Dscalar > 0:
                    # поиск нижнего предела
                    if t > 1:
                        return
                    else:
                        tLower = max(tLower, t)
                elif Dscalar < 0:
                    # поиск верхнего предела
                    if t < 0:
                        return
                    else:
                        tTop = min(tTop, t)

            # проверка фактической видимости отрезка
        print(tLower > tTop)
        if tLower <= tTop:
            self.scene.addLine(currentLine[0][0] + (currentLine[1][0] - currentLine[0][0]) * tTop,
                        currentLine[0][1] + (currentLine[1][1] - currentLine[0][1]) * tTop,
                        currentLine[0][0] + (currentLine[1][0] - currentLine[0][0]) * tLower,
                        currentLine[0][1] + (currentLine[1][1] - currentLine[0][1]) * tLower, self.pen)
            
class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        global window
        if window.inputBars or window.inputPolygon:
            window.addPoint(event.scenePos())

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    window = CutterApp()  
    window.show()
    app.exec_()
