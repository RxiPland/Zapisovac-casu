from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
from datetime import datetime
from time import sleep
from threading import Thread
import sqlite3
from os.path import exists
from datetime import date

class Ui_MainWindow_hlavnimenu(object):

    def center(self):

        # funkce, která přesune okno programu do prostřed obrazovky

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def beh_casu(self):

        # samotné zapisování času

        global pokracovat

        while pokracovat:

            now = datetime.now()
            aktualni_cas = now.strftime("%H:%M:%S")

            self.label.setText("Čas: " + aktualni_cas)

            sleep(0.5)

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


    def nazev_projektu(self, a):

        # načte jméno vybraného projektu do proměnné pro budoucí použítí

        global nazev

        nazev = str(a)

    def zapsat_zacatek(self):

        # po zmáčknutí tlačítka "zapsat začátek"

        global nazev

        existuje = exists(nazev + ".db")

        if existuje == False:

            return "DB_NEEXISTUJE"
        
        else:

            # zapisování do databáze

            now2 = datetime.now()
            aktualni_cas2 = now2.strftime("%H:%M:%S")

            datum_zadani = date.today()
            datum_zadani = date.strftime(datum_zadani, "%Y-%m-%d")

            connection = sqlite3.connect(nazev + '.db')
            cursor = connection.cursor()

            sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
            vysledek1 = cursor.execute(sqlstr).fetchall()

            id_1 = int(vysledek1[0][0])

            sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={id_1}".format(id_1=id_1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            posledni_datum_odepsani = str(vysledek1)

            connection.commit()
            cursor.close()

            if posledni_datum_odepsani != "[(None,)]":

                id_1 += 1

                while True:

                    try:

                        sqliteConnection = sqlite3.connect(nazev + '.db')
                        cursor = sqliteConnection.cursor()

                        sqlite_insert_query = "insert into tabulka(ID, Nazev, Zapsani, Zapsani_cas) values(?, ?, ?, ?)"

                        val = (int(id_1), nazev, datum_zadani, aktualni_cas2)

                        cursor.execute(sqlite_insert_query, val)
                        sqliteConnection.commit()
                        cursor.close()

                        break

                    except:
                    
                        id_1 += 1

                self.label_2.setHidden(False)

                return "OK"

            else:

                return "POSLEDNI_KONEC_NEBYL_ODEPSAN"




    def zapsat_konec(self):

        # po zmáčknutí tlačítka "zapsat konec"

        global nazev

        existuje = exists(nazev + ".db")

        if existuje == False:

            return "DB_NEEXISTUJE"
        
        else:

            try:

                connection = sqlite3.connect(nazev + '.db')
                cursor = connection.cursor()

                sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
                vysledek1 = cursor.execute(sqlstr).fetchall()

                id_1 = int(vysledek1[0][0])

                sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={id_1}".format(id_1=id_1)
                vysledek1 = cursor.execute(sqlstr).fetchall()

                posledni_datum_odepsani = str(vysledek1)


                connection.commit()
                cursor.close()

            except:

                return "DB_NEFUNGUJE"

            if posledni_datum_odepsani == "[(None,)]":


                now2 = datetime.now()
                aktualni_cas2 = now2.strftime("%H:%M:%S")

                datum_odepsani = date.today()
                datum_odepsani = date.strftime(datum_odepsani, "%Y-%m-%d")

                list_prikazu = ["Odepsani", "Odepsani_cas"]
                list_hodnot = [datum_odepsani, aktualni_cas2]



                sqliteConnection = sqlite3.connect(nazev + '.db')
                cursor = sqliteConnection.cursor()

                pocitadlo1 = int(0)

                for word in list_prikazu:

                    sqlite_insert_query = "UPDATE tabulka SET {word}='{hodnoty}' WHERE ID={id_1}".format(word=word, hodnoty=list_hodnot[pocitadlo1], id_1=id_1)
 
                    cursor.execute(sqlite_insert_query)

                    pocitadlo1 += 1


                sqliteConnection.commit()
                cursor.close()

                self.label_2.setHidden(True)

                return "OK"

            else:

                return "POSLEDNI_KONEC_BYL_ZAPSAN"



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
        self.pushButton.setText(_translate("MainWindow", "Zapsat začátek"))
        self.pushButton_2.setText(_translate("MainWindow", "Zapsat konec"))
        self.pushButton_3.setText(_translate("MainWindow", "Admin"))
        self.label.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "Stav: konec není zapsán"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_hlavnimenu()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
