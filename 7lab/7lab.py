import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtCore
from math import sqrt
import design

now = None

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
        
        self.inputBars = False
        self.inputRect = False
        
        self.lines = []
        self.lastPoint = None
        
        self.colorInRect = QtCore.Qt.red
        self.colorOutRect = QtCore.Qt.blue
        
        self.rect = None

    def clearScene(self):
        self.scene.clear()
        self.listWidget.clear()
        self.inputBars = False
        self.inputRect = False
        self.lines = []
        self.lastPoint = None
        
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
        global now
        if self.inputRect:
            if now != None:
                buf = self.scene.itemAt(now, QtGui.QTransform()).rect()
                self.rect = [buf.left(), buf.top(), buf.right(), buf.bottom()]
                print(self.rect)
            self.inputRect = False
            self.pushButton.setDisabled(False)
            self.pushButton_3.setDisabled(False)
            self.pushButton_4.setDisabled(False)
        else:
            now = None
            self.rect = None 
            self.inputRect = True
            self.pushButton.setDisabled(True)
            self.pushButton_3.setDisabled(True)
            self.pushButton_4.setDisabled(True)

    def addPoint(self, point):
        if self.lastPoint == None:
            self.lastPoint = point
        else:
            self.lines.append([[self.lastPoint.x(), self.lastPoint.y()], \
                                            [point.x(), point.y()]])
            x = self.lastPoint.x()
            y = self.lastPoint.y()
            self.listWidget.addItem('( (' + str(x) + ' ; ' + str(y) + ') ; (' + \
                                                    str(point.x()) + ' ; ' + str(point.y()) + ') )')
            self.pen.setColor(QtCore.Qt.black)
            self.scene.addLine(x, y, point.x(), point.y(), self.pen)
            self.lastPoint = None    
    
    def cutScene(self):
        if (self.lines != [] and self.rect != None):
            for j in range(0, len(self.lines)): 
                eps = 1e-4
                i = 1
                P1 = QtCore.QPointF(self.lines[j][0][0], self.lines[j][0][1])
                P2 = QtCore.QPointF(self.lines[j][1][0], self.lines[j][1][1])
                T1 = [0 for i in range(4)]
                T2 = [0 for i in range(4)]
                S1 = 0
                S2 = 0
                while True:
                    print(1)
                    T1 = setBits(self.rect, P1, T1)
                    T2 = setBits(self.rect, P2, T2)

                    S1 = getSum(T1)
                    S2 = getSum(T2)
                    
                    if S1 == 0 and S2 == 0:
                        self.pen.setColor(self.colorInRect)
                        self.scene.addLine(P1.x(), P1.y(), P2.x(), P2.y(), self.pen)
                        break
                    
                    
                    R = QtCore.QPointF()
                
                    if logicMult(T1, T2) == 0:
                        R = P1
                        if i > 2:
                            if  logicMult(T1, T2) == 0:
                                self.pen.setColor(self.colorInRect)
                                self.scene.addLine(P1.x(), P1.y(), P2.x(), P2.y(), self.pen)
                                break
                            else:
                                break
                    
                        while (abs(P1.x() - P2.x()) > eps or abs(P1.y() - P2.y()) > eps):
                            Pcp = QtCore.QPointF()
                            Pcp.setX((P1.x() + P2.x()) / 2)
                            Pcp.setY((P1.y() + P2.y()) / 2)
                            Pm = P1
                            P1 = Pcp
                            T1 = setBits(self.rect, P1, T1)
                            pr = logicMult(T1, T2)
                            if pr != 0:
                                P1 = Pm
                                P2 = Pcp 
                        P1 = P2
                        P2 = R
                        i += 1     
            
def logicMult(arrFirst, arrSecond):
    res = 0
    for i in range(4):
        res += arrFirst[i] * arrSecond[i]
    return res
                    
def getSum(arr):
    res = 0
    for i in range(len(arr)):
        res += arr[i]
    return res

def minAndMax(rect):
    if rect[1] > rect[3]:
        minY = rect[3]
        maxY = rect[1]
    else:
        minY = rect[1]
        maxY= rect[3]
        
    if rect[0] > rect[2]:
        minX = rect[2]
        maxX = rect[0]
    else:
        minX = rect[0]
        maxX = rect[2]
    return minX, maxX, minY, maxY

         
def setBits(rect, point, arr):
    x = point.x()
    y = point.y()
    minX, maxX, minY, maxY = minAndMax(rect)
    arr[3] = 1 if x < minX else 0
    arr[2] = 1 if x > maxX else 0
    arr[1] = 1 if y < minY else 0
    arr[0] = 1 if y > maxY else 0
    return arr             


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        global window
        if window.inputBars:
            window.addPoint(event.scenePos())
    
    def mouseMoveEvent(self, event):
        global window, now
        if window.inputRect:
            if now is None:
                now = event.scenePos()
            else:
                self.removeItem(self.itemAt(now, QtGui.QTransform()))
                points = event.scenePos()
                self.addRect(now.x(), now.y(), abs(now.x() - points.x()), abs(now.y() - points.y()))

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    window = CutterApp()  
    window.show()
    app.exec_()
