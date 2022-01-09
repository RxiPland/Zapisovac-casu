from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox
import sqlite3
from os.path import exists
import datetime
import webbrowser

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



    def udelat_hezci_datum(self, datum):

        # 8003 days, 19:30:31

        if "days," in datum:

            datum = datum.replace("days,", "dní")

            # 8003 dní 19:30:31

            datum_char = list(datum)

            pocitadlo1 = 1
            pismena_string = ""

            for char in datum_char:

                if char != " " or pocitadlo1 != 1:

                    pismena_string = pismena_string + char

                elif char == " " and pocitadlo1 == 1:

                    pocitadlo1 = 0

            datum = str(pismena_string)

            

        # 8003dní 19:30:31

        datum_char_list = list(datum)

        pocitadlo2 = 1

        pismena_string = ""


        for char in datum_char_list:

            if char != ":":

                pismena_string = pismena_string + char

            elif char == ":":

                if pocitadlo2 == 1:

                    pismena_string = pismena_string + "h "

                    pocitadlo2 = 2

                elif pocitadlo2 == 2:

                    pismena_string = pismena_string + "min "

        pismena_string = pismena_string + "s"

        # 8003dní 19h 30min 31s

        return str(pismena_string)


    def predelat_cas(self, a, b):

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

        if b == "rozdelene":

            cas_finalni = [hodiny, minuty, vteriny]

        else:

            cas_finalni = (hodiny*60*60) + (minuty*60) + vteriny

        return cas_finalni

        


    def predelat_datum(self, a, b):

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

        den = int(list_pismen_hotovo[1])
        mesic = int(list_pismen_hotovo[2])
        rok = int(list_pismen_hotovo[0])

        if b != "rozdelene":

            finalni_string = str(den) + "." + str(mesic) + "." + str(rok)

        else:

            finalni_string = [den, mesic, rok]


        return finalni_string

    


    def vypocitat_celkovy_cas(self, prvniId, posledniId):

        connection = sqlite3.connect(nazev + '.db')
        cursor = connection.cursor()

        pocitadlo1 = prvniId

        sqlstr = "SELECT Zapsani FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
        vysledek1 = cursor.execute(sqlstr).fetchall()

        vysledek1 = vysledek1[0][0] # datum

        datum1_zapsani = self.predelat_datum(vysledek1, "rozdelene")


        sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
        vysledek1 = cursor.execute(sqlstr).fetchall()

        vysledek1 = vysledek1[0][0] # datum


        datum1_odepsani = self.predelat_datum(vysledek1, "rozdelene")



        sqlstr = "SELECT Zapsani_cas FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
        vysledek1 = cursor.execute(sqlstr).fetchall()

        vysledek1 = vysledek1[0][0]

        posledni_zacatek_cas = str(vysledek1) # čas

        predelany_cas_zacatek = self.predelat_cas(posledni_zacatek_cas, "rozdelene")


        sqlstr = "SELECT Odepsani_cas FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
        vysledek1 = cursor.execute(sqlstr).fetchall()

        vysledek1 = vysledek1[0][0]

        posledni_konec_cas = str(vysledek1) # čas

        predelany_cas_konec = self.predelat_cas(posledni_konec_cas, "rozdelene")



        datum1_zapsani_dny = datetime.datetime(datum1_zapsani[2], datum1_zapsani[0], datum1_zapsani[1], predelany_cas_zacatek[0], predelany_cas_zacatek[1], predelany_cas_zacatek[2])

        datum1_odepsani_dny = datetime.datetime(datum1_odepsani[2], datum1_odepsani[0], datum1_odepsani[1], predelany_cas_konec[0], predelany_cas_konec[1], predelany_cas_konec[2])


        finalni_cas = (datum1_odepsani_dny - datum1_zapsani_dny)

        pocitadlo1 += 1

        while pocitadlo1 <= posledniId:


            sqlstr = "SELECT Zapsani FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0] # datum

            datum1_zapsani = self.predelat_datum(vysledek1, "rozdelene")


            sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0] # datum


            datum1_odepsani = self.predelat_datum(vysledek1, "rozdelene")



            sqlstr = "SELECT Zapsani_cas FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_zacatek_cas = str(vysledek1) # čas

            predelany_cas_zacatek = self.predelat_cas(posledni_zacatek_cas, "rozdelene")


            sqlstr = "SELECT Odepsani_cas FROM tabulka WHERE ID={vybrane_id}".format(vybrane_id=pocitadlo1)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            posledni_konec_cas = str(vysledek1) # čas

            predelany_cas_konec = self.predelat_cas(posledni_konec_cas, "rozdelene")



            datum1_zapsani_dny = datetime.datetime(datum1_zapsani[2], datum1_zapsani[0], datum1_zapsani[1], predelany_cas_zacatek[0], predelany_cas_zacatek[1], predelany_cas_zacatek[2])

            datum1_odepsani_dny = datetime.datetime(datum1_odepsani[2], datum1_odepsani[0], datum1_odepsani[1], predelany_cas_konec[0], predelany_cas_konec[1], predelany_cas_konec[2])


            finalni_cas = finalni_cas + (datum1_odepsani_dny - datum1_zapsani_dny)

            pocitadlo1 += 1


        connection.commit()
        cursor.close()


        return str(finalni_cas)
    


    def info_v_text_editu(self):

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


            sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={posledni_id}".format(posledni_id=posledni_id)
            vysledek1 = cursor.execute(sqlstr).fetchall()

            vysledek1 = vysledek1[0][0]

            try:

                posledni_datum_odepsani1 = str(vysledek1)

                if posledni_datum_odepsani1 == "None":

                    posledni_datum_odepsani1 = "ZADNE_NENI"


            except:

                posledni_datum_odepsani1 = "ZADNE_NENI"


            if posledni_datum_odepsani1 == "ZADNE_NENI":

                celkovy_pocet_koncu = int(celkovy_pocet_zacatku) - 1

            else:

                celkovy_pocet_koncu = int(celkovy_pocet_zacatku)


            posledni_zacatek = self.predelat_datum(posledni_zacatek, "")
            posledni_konec = self.predelat_datum(posledni_konec, "")
            prvni_zacatek = self.predelat_datum(prvni_zacatek, "")


            celkovy_cas = self.vypocitat_celkovy_cas(prvni_id, posledni_id)

            celkovy_cas = self.udelat_hezci_datum(celkovy_cas)

            
            self.plainTextEdit.setPlainText("Celkový odpracovaný čas: {celkovy_cas}\n\n\nPoslední začátek: {posledni_zacatek}\nPoslední konec: {posledni_konec}\n\n\nDatum úplně prvního začátku: {prvni_zacatek}\n\n\nCelkový počet začátků: {celkovy_pocet_zacatku}\nCelkový počet konců: {celkovy_pocet_koncu}".format(celkovy_cas = celkovy_cas, posledni_zacatek = posledni_zacatek + " " + posledni_zacatek_cas, posledni_konec = posledni_konec + " " + posledni_konec_cas, prvni_zacatek = prvni_zacatek +  " " + prvni_zacatek_cas, celkovy_pocet_zacatku = celkovy_pocet_zacatku, celkovy_pocet_koncu = celkovy_pocet_koncu))



        except:

            self.plainTextEdit.setPlainText("Nastala chyba při výpočtu statistik!")
    



    def zdrojovy_kod(self):

        webbrowser.open("https://github.com/RxiPland/zapisovac-casu")


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
        self.pushButton_2.setGeometry(QtCore.QRect(20, 330, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")


        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(380, 330, 101, 41))
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

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(210, 330, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_5.clicked.connect(self.zdrojovy_kod)


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
        self.pushButton_5.setText(_translate("MainWindow", "Zdrojový kód"))

