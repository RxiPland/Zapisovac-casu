from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
from datetime import datetime
from time import sleep
from threading import Thread

class Ui_MainWindow_hlavnimenu(object):



    def beh_casu(self):

        # samotné zapisování času

        global pokracovat

        while pokracovat:

            now = datetime.now()
            aktualni_cas = now.strftime("%H:%M:%S")

            self.label.setText("Čas: " + aktualni_cas)

            sleep(1)

    def zacit_cas(self):

        # slouží pro zapnutí času

        global pokracovat

        pokracovat = True

        t = Thread(target=self.beh_casu)
        t.start()


    def ukoncit(self):

        # nastaví proměnnou pokracovat na False, takže smyčka pro čas se ukončí

        # tahle funkce se aktivuje když se zavře okno

        # funkce se aktivuje z main.py

        global pokracovat

        pokracovat = False


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


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(497, 222)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 130, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(43, 184, 241, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setHidden(True)


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 30, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 110, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")


        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hlavní menu"))
        self.pushButton.setText(_translate("MainWindow", "Zapsat start"))
        self.pushButton_2.setText(_translate("MainWindow", "Odepsat konec"))
        self.pushButton_3.setText(_translate("MainWindow", "Admin"))
        self.label.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "Poslední konec nebyl odepsán!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_hlavnimenu()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
