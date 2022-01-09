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


    def predelat_cas(self, a):

        list_pismen = list(a)

        pismena_string = ""

        list_pismen_hotovo = []

        for char in list_pismen:

            if char != ":":

                pismena_string = pismena_string + char

            elif char == ":":

                list_pismen_hotovo.append(pismena_string)
                pismena_string = ""

        list_pismen_hotovo.append(pismena_string)

        hodiny = int(list_pismen_hotovo[0])
        minuty = int(list_pismen_hotovo[1])
        vteriny = int(list_pismen_hotovo[2])

        cas_vteriny = (hodiny*60*60) + (minuty*60) + vteriny

        return cas_vteriny

        


    def predelat_datum(self, a):

        list_pismen = list(a)

        pismena_string = ""

        list_pismen_hotovo = []

        for char in list_pismen:

            if char != "-":

                pismena_string = pismena_string + char

            elif char == "-":

                list_pismen_hotovo.append(pismena_string)
                pismena_string = ""

        list_pismen_hotovo.append(pismena_string)

        den = list_pismen_hotovo[1]
        mesic = list_pismen_hotovo[2]
        rok = list_pismen_hotovo[0]

        finalni_string = den + "." + mesic + "." + rok

        return finalni_string

    


    def vypocitat_celkovy_cas(self, prvniId, posledniId):

        connection = sqlite3.connect(nazev + '.db')
        cursor = connection.cursor()

        pocitadlo1 = prvniId

        finalni_cas = 0

        while pocitadlo1 <= posledniId:

            sqlstr = "SELECT Zapsani_cas FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_zacatek_cas = str(vysledek1) # čas

            predelany_cas_zacatek = self.predelat_cas(posledni_zacatek_cas)


            sqlstr = "SELECT Odepsani_cas FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_konec_cas = str(vysledek1) # čas

            predelany_cas_konec = self.predelat_cas(posledni_konec_cas)

            finalni_cas = int(finalni_cas) + int(predelany_cas_konec-predelany_cas_zacatek)

            pocitadlo1 += 1


        connection.commit()
        cursor.close()

        return str(finalni_cas) + "s"
    
    def info_v_text_editu(self):

        #celkovy_odpracovany_cas - funguje pouze když se vejde do jednoho dne (když projde přes půlnoc - nefunguje)

        # posledni_zacatek - MÁM

        # posledni_konec - MÁM

        # datum_prvniho_zacatku - MÁM

        # celkovy_pocet_zacatku - MÁM

        # celkovy_pocet_koncu - MÁM


        try:

            connection = sqlite3.connect(nazev + '.db')
            cursor = connection.cursor()

            sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
            vysledek1 = cursor.execute(sqlstr).fetchall()

            posledni_id = int(vysledek1[0][0])


            sqlstr = "SELECT * FROM tabulka ORDER BY ID LIMIT 1"
            vysledek1 = cursor.execute(sqlstr).fetchall()

            prvni_id = int(vysledek1[0][0])


            sqlstr = "SELECT Zapsani FROM tabulka WHERE ID={posledni_id}".format(posledni_id=posledni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_zacatek = str(vysledek1) # datum


            sqlstr = "SELECT Zapsani_cas FROM tabulka WHERE ID={posledni_id}".format(posledni_id=posledni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_zacatek_cas = str(vysledek1) # čas


            sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={posledni_id}".format(posledni_id=posledni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_konec = str(vysledek1) # datum

            sqlstr = "SELECT Odepsani_cas FROM tabulka WHERE ID={posledni_id}".format(posledni_id=posledni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_konec_cas = str(vysledek1) # čas


            sqlstr = "SELECT Zapsani FROM tabulka WHERE ID={prvni_id}".format(prvni_id=prvni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            prvni_zacatek = str(vysledek1) # datum
            

            sqlstr = "SELECT Zapsani_cas FROM tabulka WHERE ID={prvni_id}".format(prvni_id=prvni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            prvni_zacatek_cas = str(vysledek1) # čas




            celkovy_pocet_zacatku = int(posledni_id)

            celkovy_pocet_koncu = int(posledni_id)


            posledni_zacatek = self.predelat_datum(posledni_zacatek)
            posledni_konec = self.predelat_datum(posledni_konec)
            prvni_zacatek = self.predelat_datum(prvni_zacatek)


            celkovy_cas = self.vypocitat_celkovy_cas(prvni_id, posledni_id)

            
            self.plainTextEdit.setPlainText("Celkový odpracovaný čas: {celkovy_cas}\n\n\nPoslední začátek: {posledni_zacatek}\nPoslední konec: {posledni_konec}\n\n\nDatum úplně prvního začátku: {prvni_zacatek}\n\n\nCelkový počet začátků: {celkovy_pocet_zacatku}\nCelkový počet konců: {celkovy_pocet_koncu}".format(celkovy_cas = celkovy_cas, posledni_zacatek = posledni_zacatek + " " + posledni_zacatek_cas, posledni_konec = posledni_konec + " " + posledni_konec_cas, prvni_zacatek = prvni_zacatek +  " " + prvni_zacatek_cas, celkovy_pocet_zacatku = celkovy_pocet_zacatku, celkovy_pocet_koncu = celkovy_pocet_koncu))



        except:

            self.plainTextEdit.setPlainText("Pro vypočítání informací musíte provést alespoň první zapsání začátku a konce!")
        


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

