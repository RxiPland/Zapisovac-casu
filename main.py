
# Udělal RxiPland


from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QMainWindow, QApplication
from PyQt5.QtWidgets import QMessageBox
from vyber_databaze import Ui_MainWindow_Vyber_db
from vytvorit_novou_db import Ui_MainWindow_Vytvorit_novou_databazi
from admin import Ui_MainWindow_admin_panel
from hlavni_menu import Ui_MainWindow_hlavnimenu
from os import execl
from os.path import exists
import sqlite3


class vybrani_databaze(QMainWindow, Ui_MainWindow_Vyber_db):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


    def tlacitko_zpet(self):

        # tlačítko zpět v přidat nový projekt

        vytvorit_novou.close()
        self.pridat_policka("nepridavat")
        self.dosadit_nazev_do_boxu()
        vytvorit_novou.lineEdit.clear()
        vytvorit_novou.lineEdit_2.clear()
        self.pro_zacatek()


    def pro_zacatek(self):

        # slouží pro otevření okna

        if self.pridat_policka("nepridavat") == "ZADNE_DB_K_DISPOZICI":
            
            # argument "nepridavat" slouží pro to, aby funkce nepřidávala nové hodnoty do boxu, tenhle if slouží pouze pro ověření

            vyber_db1.show()
            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Chyba!")
            msgBox.setText("Program nenašel žádný existující projekt.\n\nOtevře se okno s vytvořením.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            vytvorit_novou.otevrit_okno()


        else:

            vyber_db1.center()
            vytvorit_novou.center()
            vyber_db1.show()



    def potvrdit_nacteni_databaze(self):

        # když v menu, kde se vybírají projekty, vyberete jméno z boxu

        obsah_boxu = str(self.comboBox.currentText())

        existuje = exists(obsah_boxu + ".db")

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle("Oznámení")
        msgBox.setText("Opravdu chcete načíst projekt: " + obsah_boxu )
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = msgBox.button(QMessageBox.Yes)
        buttonY.setText("Ano")
        buttonN = msgBox.button(QMessageBox.No)
        buttonN.setText("Zrušit")

        returnValue = msgBox.exec()


        if returnValue == QMessageBox.Yes:

            if existuje == False:

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("Problém!")
                msgBox.setText("Databáze neexistuje! Provedu restart.")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

                python = sys.executable
                execl(python, python, * sys.argv)

            elif existuje == True:

                try:

                    connection = sqlite3.connect(obsah_boxu + '.db')
                    cursor = connection.cursor()

                    sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
                    vysledek1 = cursor.execute(sqlstr).fetchall()

                    id_1 = int(vysledek1[0][0])

                    sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={id_1}".format(id_1=id_1)
                    vysledek1 = cursor.execute(sqlstr).fetchall()

                    posledni_datum_odepsani = str(vysledek1)

                    connection.commit()
                    cursor.close()

                    if posledni_datum_odepsani == "[(None,)]":

                        hl_menu.label_2.setHidden(False)

                    else:

                        hl_menu.label_2.setHidden(True)

                except:

                    hl_menu.label_2.setHidden(True)


                vyber_db1.close()
                vyber_db1.center()

                hl_menu.nazev_projektu(obsah_boxu)

                hl_menu.zacit_cas()
                hl_menu.center()
                hl_menu.show()
                

        if returnValue == QMessageBox.No:

            return

   

class vytvorit_databazi(QMainWindow, Ui_MainWindow_Vytvorit_novou_databazi):

    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)



    def otevrit_okno(self):

        # otevře se okno s vytvářením nové databáze(projektu)
        
        vyber_db1.close()
        vyber_db1.center()
        vytvorit_novou.center()
        vytvorit_novou.show()


    def vytvorit_databazi(self):

        # chybové hlášky

        # pokud žádná chyba nebude, program se restartuje, aby se načetli všechny databáze do boxu

        if self.vytvorit_db() == "DB_EXISTUJE":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Tenhle název už existuje!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        elif self.vytvorit_db() == "NEMA_NAZEV":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Vyplňte název!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        else:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Vytvoření proběhlo úspěšně, restartuji program.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            python = sys.executable
            execl(python, python, * sys.argv)

class hlavni_menu(QMainWindow, Ui_MainWindow_hlavnimenu):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


    def kontrola_chyb_zacatek(self):

        chyby_zacatek = self.zapsat_zacatek()

        if chyby_zacatek == "DB_NEEXISTUJE":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Databáze neexistuje!\n\nVytvořte novou.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            python = sys.executable
            execl(python, python, * sys.argv)

        elif chyby_zacatek == "POSLEDNI_KONEC_NEBYL_ZAPSAN":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Poslední konec nebyl zapsán!\n\nProblém vyřešíte tím, že zapíšete konec")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()


        elif chyby_zacatek == "OK":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Čas začátku byl zapsán")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



    def kontrola_chyb_konec(self):

        chyby_konec = self.zapsat_konec()

        if chyby_konec == "DB_NEEXISTUJE":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Databáze neexistuje!\n\nVytvořte novou.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            python = sys.executable
            execl(python, python, * sys.argv)

        elif chyby_konec == "POSLEDNI_KONEC_BYL_UZ_ZAPSAN":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Konec je už zapsaný od předchozího zápisu!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        

        elif chyby_konec == "DB_NEFUNGUJE":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Problém!")
            msgBox.setText("Databáze nefunguje")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        elif chyby_konec == "OK":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Čas ukončení byl zapsán")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



class admin_panel(QMainWindow, Ui_MainWindow_admin_panel):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
    
    def admin_panel_start(self):

        nazev = str(vyber_db1.comboBox.currentText())

        self.nazev_projektu(nazev)
        
        hl_menu.close()
        hl_menu.center()
        admin1.center()
        admin1.show()

    def tlacitko_odejit(self):

        admin1.close()
        admin1.center()
        hl_menu.center()
        hl_menu.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    vyber_db1 = vybrani_databaze()
    vytvorit_novou = vytvorit_databazi()
    hl_menu = hlavni_menu()
    admin1 = admin_panel()
    vyber_db1.pro_zacatek()
    vyber_db1.pushButton.clicked.connect(vytvorit_novou.otevrit_okno)
    vyber_db1.comboBox.activated.connect(vyber_db1.potvrdit_nacteni_databaze)
    vytvorit_novou.pushButton.clicked.connect(vytvorit_novou.vytvorit_databazi)
    vytvorit_novou.pushButton_2.clicked.connect(vyber_db1.tlacitko_zpet)
    hl_menu.pushButton.clicked.connect(hl_menu.kontrola_chyb_zacatek)
    hl_menu.pushButton_2.clicked.connect(hl_menu.kontrola_chyb_konec)
    hl_menu.pushButton_3.clicked.connect(admin1.admin_panel_start)
    admin1.pushButton_3.clicked.connect(admin1.tlacitko_odejit)
    app.aboutToQuit.connect(hl_menu.ukoncit)
    sys.exit(app.exec_())