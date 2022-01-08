from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
from os.path import exists
import sqlite3
import hashlib


class Ui_MainWindow_Vytvorit_novou_databazi(object):

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    def vytvorit_db(self):

        # vytvoří databázi a textový soubor s hashem hesla

        nazev =  str(self.lineEdit.text())
        heslo = str(self.lineEdit_2.text())

        existuje = exists(nazev + ".db")

        if nazev == "":

            return "NEMA_NAZEV"

        elif existuje == True:

            return "DB_EXISTUJE"


        else:

            sqliteConnection = sqlite3.connect(nazev + ".db")
            cursor = sqliteConnection.cursor()

            VytvoritTabulku = "CREATE TABLE 'tabulka' ('ID' INT PRIMARY KEY NOT NULL, Nazev TEXT, Zapsani DATE, Zapsani_cas TEXT, Odepsani DATE, Odepsani_cas Text)"

            cursor.execute(VytvoritTabulku)

            sqliteConnection.commit()
            cursor.close()

            if heslo == "":

                with open(nazev + "_password", "w") as output:

                    output.write(str("BEZHESLA"))


            else:

                hash_hesla = hashlib.sha256(heslo.encode())
                hex_dig = hash_hesla.hexdigest()

                with open(nazev + "_password", "w") as output:

                    output.write(str(hex_dig))


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(470, 195)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(31, 24, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(31, 110, 261, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 67, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 116, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")


        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 50, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(100)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("např. Programování")


        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 133, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(100)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("nechte prázdné pro žádné heslo")


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vytvořit nový projekt"))
        self.label.setText(_translate("MainWindow", "Zadejte název projektu:"))
        self.pushButton.setText(_translate("MainWindow", "Vytvořit"))
        self.pushButton_2.setText(_translate("MainWindow", "Odejít zpět"))
        self.label_2.setText(_translate("MainWindow", "Heslo pro přístup k admin panelu:"))

        self.center()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_Vytvorit_novou_databazi()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
