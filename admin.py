from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
import sqlite3
from os.path import exists
from datetime import date

class Ui_MainWindow_admin_panel(object):


    def center(self):

        # funkce, která přesune okno programu do prostřed obrazovky

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    
    def nazev_projektu(self, a):

        # načte jméno vybraného projektu do proměnné pro budoucí použítí

        global nazev

        nazev = str(a)

        self.label_2.setText("Aktuálně vybraný projekt: " + nazev)

    
    def info_v_text_editu(self):

        pass




    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(509, 395)

        MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(22, 80, 208, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(22, 30, 481, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 280, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 330, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")


        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(380, 328, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")


        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(150, 280, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")


        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 110, 401, 151))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Admin panel"))
        self.pushButton.setText(_translate("MainWindow", "Změnit heslo"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Celkový odpracovaný čas: \n\n\nPoslední začátek: \nPoslední konec: \n\n\nDatum prvního začátku: \n\n\nCelkový počet začátků: \nCelkový počet konců: "))
        self.label.setText(_translate("MainWindow", "Statistiky:"))
        self.pushButton_2.setText(_translate("MainWindow", "Vymazat databázi i s daty"))
        self.pushButton_3.setText(_translate("MainWindow", "Odejít"))
        self.label_2.setText(_translate("MainWindow", "Aktuálně vybraný projekt:"))
        self.pushButton_4.setText(_translate("MainWindow", "Změnit název projektu"))

