# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1119, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 1121, 671))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 680, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 680, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 710, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(160, 710, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.xCenterCircle = QtWidgets.QLineEdit(self.centralwidget)
        self.xCenterCircle.setGeometry(QtCore.QRect(70, 710, 31, 22))
        self.xCenterCircle.setObjectName("xCenterCircle")
        self.yCenterCircle = QtWidgets.QLineEdit(self.centralwidget)
        self.yCenterCircle.setGeometry(QtCore.QRect(110, 710, 31, 22))
        self.yCenterCircle.setObjectName("yCenterCircle")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 740, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.radiusCircle = QtWidgets.QLineEdit(self.centralwidget)
        self.radiusCircle.setGeometry(QtCore.QRect(70, 740, 31, 22))
        self.radiusCircle.setObjectName("radiusCircle")
        self.drawCircle = QtWidgets.QPushButton(self.centralwidget)
        self.drawCircle.setGeometry(QtCore.QRect(10, 770, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.drawCircle.setFont(font)
        self.drawCircle.setObjectName("drawCircle")
        self.yCenterEllipse = QtWidgets.QLineEdit(self.centralwidget)
        self.yCenterEllipse.setGeometry(QtCore.QRect(270, 710, 31, 22))
        self.yCenterEllipse.setObjectName("yCenterEllipse")
        self.xCenterEllipse = QtWidgets.QLineEdit(self.centralwidget)
        self.xCenterEllipse.setGeometry(QtCore.QRect(230, 710, 31, 22))
        self.xCenterEllipse.setObjectName("xCenterEllipse")
        self.coefA = QtWidgets.QLineEdit(self.centralwidget)
        self.coefA.setGeometry(QtCore.QRect(230, 740, 31, 22))
        self.coefA.setText("")
        self.coefA.setObjectName("coefA")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(160, 740, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.coefB = QtWidgets.QLineEdit(self.centralwidget)
        self.coefB.setGeometry(QtCore.QRect(270, 740, 31, 22))
        self.coefB.setText("")
        self.coefB.setObjectName("coefB")
        self.drawEllipse = QtWidgets.QPushButton(self.centralwidget)
        self.drawEllipse.setGeometry(QtCore.QRect(160, 770, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.drawEllipse.setFont(font)
        self.drawEllipse.setObjectName("drawEllipse")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(310, 680, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(310, 710, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.stepSpektor = QtWidgets.QLineEdit(self.centralwidget)
        self.stepSpektor.setGeometry(QtCore.QRect(450, 710, 41, 22))
        self.stepSpektor.setObjectName("stepSpektor")
        self.countCircles = QtWidgets.QLineEdit(self.centralwidget)
        self.countCircles.setGeometry(QtCore.QRect(450, 740, 41, 22))
        self.countCircles.setObjectName("countCircles")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(310, 740, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.drawCircleSpector = QtWidgets.QPushButton(self.centralwidget)
        self.drawCircleSpector.setGeometry(QtCore.QRect(310, 770, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.drawCircleSpector.setFont(font)
        self.drawCircleSpector.setObjectName("drawCircleSpector")
        self.drawEllipseSpector = QtWidgets.QPushButton(self.centralwidget)
        self.drawEllipseSpector.setGeometry(QtCore.QRect(400, 770, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.drawEllipseSpector.setFont(font)
        self.drawEllipseSpector.setObjectName("drawEllipseSpector")
        self.canonEquation = QtWidgets.QRadioButton(self.centralwidget)
        self.canonEquation.setGeometry(QtCore.QRect(520, 680, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.canonEquation.setFont(font)
        self.canonEquation.setObjectName("canonEquation")
        self.paramEquation = QtWidgets.QRadioButton(self.centralwidget)
        self.paramEquation.setGeometry(QtCore.QRect(520, 700, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.paramEquation.setFont(font)
        self.paramEquation.setObjectName("paramEquation")
        self.methodBrezenhem = QtWidgets.QRadioButton(self.centralwidget)
        self.methodBrezenhem.setGeometry(QtCore.QRect(520, 720, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.methodBrezenhem.setFont(font)
        self.methodBrezenhem.setObjectName("methodBrezenhem")
        self.methodMidpoint = QtWidgets.QRadioButton(self.centralwidget)
        self.methodMidpoint.setGeometry(QtCore.QRect(520, 740, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.methodMidpoint.setFont(font)
        self.methodMidpoint.setObjectName("methodMidpoint")
        self.libraryMethod = QtWidgets.QRadioButton(self.centralwidget)
        self.libraryMethod.setGeometry(QtCore.QRect(520, 760, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.libraryMethod.setFont(font)
        self.libraryMethod.setObjectName("libraryMethod")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(760, 680, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.blackScene = QtWidgets.QPushButton(self.centralwidget)
        self.blackScene.setGeometry(QtCore.QRect(760, 700, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.blackScene.setFont(font)
        self.blackScene.setObjectName("blackScene")
        self.whiteScene = QtWidgets.QPushButton(self.centralwidget)
        self.whiteScene.setGeometry(QtCore.QRect(760, 730, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.whiteScene.setFont(font)
        self.whiteScene.setObjectName("whiteScene")
        self.blueScene = QtWidgets.QPushButton(self.centralwidget)
        self.blueScene.setGeometry(QtCore.QRect(760, 760, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.blueScene.setFont(font)
        self.blueScene.setObjectName("blueScene")
        self.redScene = QtWidgets.QPushButton(self.centralwidget)
        self.redScene.setGeometry(QtCore.QRect(760, 790, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.redScene.setFont(font)
        self.redScene.setObjectName("redScene")
        self.blackLine = QtWidgets.QPushButton(self.centralwidget)
        self.blackLine.setGeometry(QtCore.QRect(870, 700, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.blackLine.setFont(font)
        self.blackLine.setObjectName("blackLine")
        self.whiteLine = QtWidgets.QPushButton(self.centralwidget)
        self.whiteLine.setGeometry(QtCore.QRect(870, 730, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.whiteLine.setFont(font)
        self.whiteLine.setObjectName("whiteLine")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(870, 680, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.redLine = QtWidgets.QPushButton(self.centralwidget)
        self.redLine.setGeometry(QtCore.QRect(870, 790, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.redLine.setFont(font)
        self.redLine.setObjectName("redLine")
        self.blueLine = QtWidgets.QPushButton(self.centralwidget)
        self.blueLine.setGeometry(QtCore.QRect(870, 760, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.blueLine.setFont(font)
        self.blueLine.setObjectName("blueLine")
        self.clearScene = QtWidgets.QPushButton(self.centralwidget)
        self.clearScene.setGeometry(QtCore.QRect(980, 750, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clearScene.setFont(font)
        self.clearScene.setObjectName("clearScene")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(980, 680, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.penWidth = QtWidgets.QLineEdit(self.centralwidget)
        self.penWidth.setGeometry(QtCore.QRect(980, 710, 31, 28))
        self.penWidth.setObjectName("penWidth")
        self.changePenWidth = QtWidgets.QPushButton(self.centralwidget)
        self.changePenWidth.setGeometry(QtCore.QRect(1020, 710, 91, 28))
        self.changePenWidth.setObjectName("changePenWidth")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.xCenterCircle, self.yCenterCircle)
        MainWindow.setTabOrder(self.yCenterCircle, self.radiusCircle)
        MainWindow.setTabOrder(self.radiusCircle, self.drawCircle)
        MainWindow.setTabOrder(self.drawCircle, self.xCenterEllipse)
        MainWindow.setTabOrder(self.xCenterEllipse, self.yCenterEllipse)
        MainWindow.setTabOrder(self.yCenterEllipse, self.coefA)
        MainWindow.setTabOrder(self.coefA, self.coefB)
        MainWindow.setTabOrder(self.coefB, self.drawEllipse)
        MainWindow.setTabOrder(self.drawEllipse, self.stepSpektor)
        MainWindow.setTabOrder(self.stepSpektor, self.countCircles)
        MainWindow.setTabOrder(self.countCircles, self.drawCircleSpector)
        MainWindow.setTabOrder(self.drawCircleSpector, self.drawEllipseSpector)
        MainWindow.setTabOrder(self.drawEllipseSpector, self.penWidth)
        MainWindow.setTabOrder(self.penWidth, self.changePenWidth)
        MainWindow.setTabOrder(self.changePenWidth, self.clearScene)
        MainWindow.setTabOrder(self.clearScene, self.libraryMethod)
        MainWindow.setTabOrder(self.libraryMethod, self.blackScene)
        MainWindow.setTabOrder(self.blackScene, self.whiteScene)
        MainWindow.setTabOrder(self.whiteScene, self.blueScene)
        MainWindow.setTabOrder(self.blueScene, self.redScene)
        MainWindow.setTabOrder(self.redScene, self.blackLine)
        MainWindow.setTabOrder(self.blackLine, self.whiteLine)
        MainWindow.setTabOrder(self.whiteLine, self.redLine)
        MainWindow.setTabOrder(self.redLine, self.blueLine)
        MainWindow.setTabOrder(self.blueLine, self.methodMidpoint)
        MainWindow.setTabOrder(self.methodMidpoint, self.paramEquation)
        MainWindow.setTabOrder(self.paramEquation, self.methodBrezenhem)
        MainWindow.setTabOrder(self.methodBrezenhem, self.graphicsView)
        MainWindow.setTabOrder(self.graphicsView, self.canonEquation)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Для окружности:"))
        self.label_2.setText(_translate("MainWindow", "Для эллипса:"))
        self.label_3.setText(_translate("MainWindow", "Центр:"))
        self.label_4.setText(_translate("MainWindow", "Центр:"))
        self.label_5.setText(_translate("MainWindow", "Радиус:"))
        self.drawCircle.setText(_translate("MainWindow", "Построить"))
        self.label_6.setText(_translate("MainWindow", "Коэф-ты:"))
        self.drawEllipse.setText(_translate("MainWindow", "Построить"))
        self.label_7.setText(_translate("MainWindow", "Построить спектр:"))
        self.label_8.setText(_translate("MainWindow", "Шаг (радиус):"))
        self.label_9.setText(_translate("MainWindow", "Количество окр-ей:"))
        self.drawCircleSpector.setText(_translate("MainWindow", "Окружности"))
        self.drawEllipseSpector.setText(_translate("MainWindow", "Эллипсы"))
        self.canonEquation.setText(_translate("MainWindow", "Каноническое ур-е"))
        self.paramEquation.setText(_translate("MainWindow", "Параметрическое ур-е"))
        self.methodBrezenhem.setText(_translate("MainWindow", "Алгоритм Брезенхема"))
        self.methodMidpoint.setText(_translate("MainWindow", "Алгоритма средней точки"))
        self.libraryMethod.setText(_translate("MainWindow", "Библиотечный метод"))
        self.label_10.setText(_translate("MainWindow", "Цвет сцены:"))
        self.blackScene.setText(_translate("MainWindow", "Черный"))
        self.whiteScene.setText(_translate("MainWindow", "Белый"))
        self.blueScene.setText(_translate("MainWindow", "Синий"))
        self.redScene.setText(_translate("MainWindow", "Красный"))
        self.blackLine.setText(_translate("MainWindow", "Черный"))
        self.whiteLine.setText(_translate("MainWindow", "Белый"))
        self.label_11.setText(_translate("MainWindow", "Цвет линии:"))
        self.redLine.setText(_translate("MainWindow", "Красный"))
        self.blueLine.setText(_translate("MainWindow", "Синий"))
        self.clearScene.setText(_translate("MainWindow", "Очистить сцену"))
        self.label_12.setText(_translate("MainWindow", "Толщина кисти:"))
        self.changePenWidth.setText(_translate("MainWindow", "Изменить"))
