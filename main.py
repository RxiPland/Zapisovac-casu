
# Udělal RxiPland


from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QMainWindow, QApplication
from PyQt5.QtWidgets import QMessageBox
from vyber_databaze import Ui_MainWindow_Vyber_db
from vytvorit_novou_db import Ui_MainWindow_Vytvorit_novou_databazi
from admin import Ui_MainWindow_admin_panel
from hlavni_menu import Ui_MainWindow_hlavnimenu
from overit_heslo import Ui_MainWindow_overit_heslo
from zmena_hesla import Ui_MainWindow_Zmena_hesla_pro_admina
from zmena_nazvu import Ui_MainWindow_Zmena_nazvu_projektu
from poznamky import Ui_MainWindow_poznamky_okno
from os import execl, remove, rename
from os.path import exists
import sqlite3
import hashlib


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

        global obsah_boxu

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
                

        elif returnValue == QMessageBox.No:

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
            msgBox.setText("Projekt s tímto názvem už existuje!")
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

        # kontroluje postup při zapisování začátku (např. pokud nebyl zapsaný konec, nenechá uživatele zapsat začátek) 

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
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Poslední konec nebyl zapsán!\n\nProblém můžete vyřešit tím, že:\n\n1) zapíšete konec\n2) smažete poslední zapsaný začátek")
            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            buttonY = msgBox.button(QMessageBox.Yes)
            buttonY.setText("Chci ho smazat")
            buttonN = msgBox.button(QMessageBox.No)
            buttonN.setText("Zapíšu ho")

            returnValue = msgBox.exec()


            if returnValue == QMessageBox.Yes:

                nazev = str(vyber_db1.comboBox.currentText())

                connection = sqlite3.connect(nazev + '.db')
                cursor = connection.cursor()

                sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
                vysledek1 = cursor.execute(sqlstr).fetchall()

                try:

                    id_1 = int(vysledek1[0][0])

                except:

                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setWindowTitle("Problém!")
                    msgBox.setText("Nastala chyba se zjišťováním posledního ID v databázi")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()


                sqlite_delete_query = ("DELETE FROM tabulka WHERE ID={id_1}".format(id_1=id_1))

                cursor.execute(sqlite_delete_query)

                connection.commit()
                cursor.close()

                hl_menu.label_2.setHidden(True)


            elif returnValue == QMessageBox.No:
                
                hl_menu.label_2.setHidden(False)

                return


        elif chyby_zacatek == "OK":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Čas začátku byl zapsán")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



    def kontrola_chyb_konec(self):

        # kontroluje jestli se může zapsat konec

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

            global obsah_boxu

            admin1.nazev_projektu(obsah_boxu)

            connection = sqlite3.connect(obsah_boxu + '.db')
            cursor = connection.cursor()

            sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
            vysledek1 = cursor.execute(sqlstr).fetchall()

            posledni_id = int(vysledek1[0][0])

            connection.commit()
            cursor.close()


            straveny_cas = admin1.vypocitat_celkovy_cas(posledni_id, posledni_id)

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Čas ukončení byl zapsán.\n\nDoba trvání, která se přičte do celkové statistiky: {straveny_cas}".format(straveny_cas=straveny_cas))
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



class admin_panel(QMainWindow, Ui_MainWindow_admin_panel):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
    
    def admin_panel_start(self):

        # otevře okno s admin panelem

        nazev = str(vyber_db1.comboBox.currentText())
    
        self.nazev_projektu(nazev)
        
        heslo_overeni.close()
        heslo_overeni.center()
        admin1.center()
        admin1.info_v_text_editu()
        admin1.show()

    def tlacitko_odejit(self):

        # tlačítko odejít v admin panelu

        admin1.close()
        admin1.center()
        hl_menu.center()
        hl_menu.show()

    
    def smazat_databazi(self):

        # tlačítko smazat projekt v admin panelu

        nazev = str(vyber_db1.comboBox.currentText())

        existujeDb = exists(nazev + ".db")
        existujeHeslo = exists(nazev + ".heslo")

        if existujeDb == False:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Databáze, kterou chcete smazat neexistuje")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        elif existujeDb == True:


            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Opravdu chcete smazat projekt: " + nazev)
            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            buttonY = msgBox.button(QMessageBox.Yes)
            buttonY.setText("Smazat")
            buttonN = msgBox.button(QMessageBox.No)
            buttonN.setText("Zrušit")

            returnValue = msgBox.exec()


            if returnValue == QMessageBox.Yes:

                remove(nazev + ".db")

                if existujeHeslo == True:

                    remove(nazev + ".heslo")

            elif returnValue == QMessageBox.No:

                return


        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle("Oznámení")
        msgBox.setText("Projekt byl úspěšně smazán.\n\nRestartuji program")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

        python = sys.executable
        execl(python, python, * sys.argv)


class overeni_hesla(QMainWindow, Ui_MainWindow_overit_heslo):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

    def odejit(self):

        # odejít z ověření hesla

        heslo_overeni.close()
        heslo_overeni.center()
        heslo_overeni.lineEdit.clear()

        hl_menu.center()
        hl_menu.show()


    def zobrazit_okno(self):

        # kontroluje, jestli může otevřít admin panel (pokud existuje heslo, otevře se nejdříve okno s ověřením hesla)

        nazev = str(vyber_db1.comboBox.currentText())
        
        connection = sqlite3.connect(nazev + '.db')
        cursor = connection.cursor()

        sqlstr = "SELECT * FROM tabulka ORDER BY ID DESC LIMIT 1"
        vysledek1 = cursor.execute(sqlstr).fetchall()

        try:

            posledni_id = int(vysledek1[0][0])

        except:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Je nutné alespoň jednou zapsat začátek a konec")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return
            

        sqlstr = "SELECT Odepsani FROM tabulka WHERE ID={posledni_id}".format(posledni_id=posledni_id)
        vysledek1 = cursor.execute(sqlstr).fetchall()

        connection.commit()
        cursor.close()

        vysledek1 = vysledek1[0][0]

        ukonceni_chyba = ""

        try:

            posledni_datum_ukonceni = str(vysledek1)

            if posledni_datum_ukonceni == "None":

                ukonceni_chyba = "ZADNE_NENI"

        except:

            ukonceni_chyba = "ZADNE_NENI"

        if ukonceni_chyba == "ZADNE_NENI":

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Pro přístup ke statistikám je nutné zapsat konec!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        else:

        

            hl_menu.close()
            hl_menu.center()

            nazev = str(vyber_db1.comboBox.currentText())

            existuje = exists(nazev + ".heslo")

            if existuje == True:

                self.lineEdit.clear()
                heslo_overeni.center()
                heslo_overeni.show()

            elif existuje == False:

                admin1.admin_panel_start()


    def overeni_hesla(self):

        # určuje, co se stane po zadání hesla (otevře se jiné okno, nebo vyskočí chyba o špatném heslu)

        global kamDal
        

        heslo = str(self.lineEdit.text())
        
        nazev = str(vyber_db1.comboBox.currentText())


        existuje = exists(nazev + ".heslo")

        if existuje == True:

            heslo_hash_open = open(nazev + ".heslo","r")
            heslo_hash = heslo_hash_open.readline()
            heslo_hash_open.close()

            hash_zadaneho_hesla = hashlib.sha256(heslo.encode())
            hex_dig = str(hash_zadaneho_hesla.hexdigest())

            if hex_dig == heslo_hash and kamDal == "ZMENA_HESLA":

                heslo_overeni.close()
                heslo_overeni.center()
                heslo_overeni.lineEdit.clear()

                zmenaHesla.lineEdit.clear()
                zmenaHesla.center()
                zmenaHesla.show()

            elif hex_dig == heslo_hash:

                admin1.admin_panel_start()

            else:

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("Chyba!")
                msgBox.setText("Heslo není správné!")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()


        elif existuje == False:
            
            admin1.admin_panel_start()



class zmena_heslaAdmin(QMainWindow, Ui_MainWindow_Zmena_hesla_pro_admina):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


    def zpetDoAdminPanelu(self):

        # jde z okna změna hesla zpět do admin panelu

        zmenaHesla.close()
        zmenaHesla.lineEdit.clear()
        zmenaHesla.center()
        admin1.center()
        admin1.show()


    def zmenit_heslo(self):

        # tohle se spustí po potvrzení nového hesla

        # + zapisuje hash hesla do textoveho dokumentu

        nove_heslo = str(zmenaHesla.lineEdit.text())
        nazev = str(vyber_db1.comboBox.currentText())

        existuje = exists(nazev + ".heslo")

        if nove_heslo == "" and existuje == True:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Od teď se přihlašujete bez hesla (heslo bylo odstraněno)")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            remove(nazev + ".heslo")

        elif nove_heslo != "" and existuje == True:

            hash_hesla = hashlib.sha256(nove_heslo.encode())
            hex_dig = hash_hesla.hexdigest()

            with open(nazev + ".heslo", "w") as output:

                output.write(str(hex_dig))

            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Staré heslo bylo změněno na nové")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        elif nove_heslo != "" and existuje == False:
            
            hash_hesla = hashlib.sha256(nove_heslo.encode())
            hex_dig = hash_hesla.hexdigest()

            with open(nazev + ".heslo", "w") as output:

                output.write(str(hex_dig))

            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Od teď se budete přihlašovat pod heslem\n\n(Dříve heslo nebylo nastaveno)")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()


        else:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Heslo není potřeba měnit\n\n(Znovu bylo zadáno prázdné pole = žádné heslo)")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()


        global kamDal

        kamDal = "NORMALNE"

        zmenaHesla.zpetDoAdminPanelu()


    def kontrola_hesla_souboru(self):

        # kontroluje, zda se nachází soubor s heslem


        nazev = str(vyber_db1.comboBox.currentText())

        existuje = exists(nazev + ".heslo")

        if existuje == True:

            admin1.close()
            admin1.center()

            global kamDal

            kamDal = "ZMENA_HESLA"

            heslo_overeni.lineEdit.clear()
            heslo_overeni.center()
            heslo_overeni.show()
        
        elif existuje == False:

            admin1.close()
            admin1.center()

            zmenaHesla.lineEdit.clear()
            zmenaHesla.center()
            zmenaHesla.show()



class zmena_nazvu_projektu(QMainWindow, Ui_MainWindow_Zmena_nazvu_projektu):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

    def zpet_do_admin_panelu(self):

        # odejde ze změny názvu zpět do admin panelu

        zmenaNazvu.close()
        zmenaNazvu.center()
        zmenaNazvu.lineEdit.clear()

        admin1.center()
        admin1.show()


    def restart_pro_zmeny(self):

        # zrestartuje celý program

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle("Oznámení")
        msgBox.setText("Pro aplikování změn provedu restart")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

        python = sys.executable
        execl(python, python, * sys.argv)


    def otevrit_okno(self):

        # otevře okno změna názvu a dosadí starý název do labelu
        
        admin1.close()
        admin1.center()

        nazev = str(vyber_db1.comboBox.currentText())

        zmenaNazvu.priradit_stary_nazev_projektu(nazev)

        zmenaNazvu.center()
        zmenaNazvu.lineEdit.clear()
        zmenaNazvu.show()


    def zmenit_nazev(self):

        # když se uživatel rozhodne změnit název projektu

        # změní se název databáze + (pokud existuje) i soubor s heslem

        nove_jmeno = str(zmenaNazvu.lineEdit.text())
        stare_jmeno = str(vyber_db1.comboBox.currentText())

        if nove_jmeno == stare_jmeno:

            # pokud se nový název rovná starému

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Chyba")
            msgBox.setText("Nový název je stejný jako starý! Vymyslete prosím nový.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return

        elif nove_jmeno != stare_jmeno and nove_jmeno != "":

            existujeDb = exists(stare_jmeno + ".db")
            existujeHeslo = exists(stare_jmeno + ".heslo")

            if existujeDb == True and existujeHeslo == True:

                # databáze i soubor s heslem existují

                try:

                    rename(stare_jmeno + ".db", nove_jmeno + ".db")
                    rename(stare_jmeno + ".heslo", nove_jmeno + ".heslo")

                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Question)
                    msgBox.setWindowTitle("Oznámení")
                    msgBox.setText("Projekt byl úspěšně přejmenován")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()

                    admin1.nazev_projektu(nove_jmeno)

                    zmenaNazvu.restart_pro_zmeny()

                except:

                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setWindowTitle("Problém")
                    msgBox.setText("Nastala chyba při změně názvů!\n\n1) Databáze byla odstraněna\n2) Název obsahuje nepovolené znaky\n3) Jiná chyba")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()

                    return



            elif existujeDb == True and existujeHeslo == False:

                # pouze databáze existuje (bez hesla)

                try:

                    rename(stare_jmeno + ".db", nove_jmeno + ".db")

                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Question)
                    msgBox.setWindowTitle("Oznámení")
                    msgBox.setText("Projekt byl úspěšně přejmenován")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()

                    admin1.nazev_projektu(nove_jmeno)

                    zmenaNazvu.restart_pro_zmeny()

                except:

                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setWindowTitle("Problém")
                    msgBox.setText("Nastala chyba při změně názvů!\n\n1) Databáze byla odstraněna\n2) Název obsahuje nepovolené znaky\n3) Jiná chyba")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()

                    return

            else:

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setWindowTitle("Problém")
                msgBox.setText("Nastala chyba při změně názvů!\n\n1) Databáze byla odstraněna\n2) Název obsahuje nepovolené znaky\n3) Jiná chyba")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

                return

        else:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Název nemůže být prázdný!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            return


class poznamky_okno(QMainWindow, Ui_MainWindow_poznamky_okno):


    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

    def otevrit_poznamky(self):

        # načte data ze souboru do poznámkového boxu

        global obsah_boxu

        admin1.close()
        admin1.center()

        try:

            poznamky_soubor = open(obsah_boxu + ".poznamky")
            poznamky_soubor_text = str(poznamky_soubor.read())
            poznamky_soubor.close()

            poznamky1.plainTextEdit.setPlainText(poznamky_soubor_text)

        except:

            poznamky1.plainTextEdit.setPlainText("")

        poznamky1.center()
        poznamky1.show()

    def zrusit(self):

        # odejde z poznámek zpět do admin panelu

        poznamky1.close()
        poznamky1.center()
        poznamky1.plainTextEdit.clear()

        admin1.center()
        admin1.show()


    def zapsat_do_souboru(self):

        # zapíše text z boxu s poznámkami do souboru

        global obsah_boxu

        try:

            with open(obsah_boxu + ".poznamky", "w") as output:

                output.write(str(poznamky1.plainTextEdit.toPlainText()))

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setWindowTitle("Oznámení")
            msgBox.setText("Uložení proběhlo v pořádku")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

            poznamky1.zrusit()

        except:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Problém")
            msgBox.setText("Nastala chyba s ukládáním!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    vyber_db1 = vybrani_databaze()
    vytvorit_novou = vytvorit_databazi()
    hl_menu = hlavni_menu()
    admin1 = admin_panel()
    heslo_overeni = overeni_hesla()
    zmenaHesla = zmena_heslaAdmin()
    zmenaNazvu = zmena_nazvu_projektu()
    poznamky1 = poznamky_okno()
    global kamDal
    kamDal = "NORMAL"
    vyber_db1.pro_zacatek()
    vyber_db1.pushButton.clicked.connect(vytvorit_novou.otevrit_okno)
    vyber_db1.comboBox.activated.connect(vyber_db1.potvrdit_nacteni_databaze)
    vytvorit_novou.pushButton.clicked.connect(vytvorit_novou.vytvorit_databazi)
    vytvorit_novou.pushButton_2.clicked.connect(vyber_db1.tlacitko_zpet)
    hl_menu.pushButton.clicked.connect(hl_menu.kontrola_chyb_zacatek)
    hl_menu.pushButton_2.clicked.connect(hl_menu.kontrola_chyb_konec)
    hl_menu.pushButton_3.clicked.connect(heslo_overeni.zobrazit_okno)
    admin1.pushButton.clicked.connect(zmenaHesla.kontrola_hesla_souboru)
    admin1.pushButton_2.clicked.connect(admin1.smazat_databazi)
    admin1.pushButton_3.clicked.connect(admin1.tlacitko_odejit)
    admin1.pushButton_4.clicked.connect(zmenaNazvu.otevrit_okno)
    admin1.pushButton_6.clicked.connect(poznamky1.otevrit_poznamky)
    heslo_overeni.pushButton.clicked.connect(heslo_overeni.overeni_hesla)
    heslo_overeni.pushButton_2.clicked.connect(heslo_overeni.odejit)
    heslo_overeni.lineEdit.returnPressed.connect(heslo_overeni.overeni_hesla)
    zmenaHesla.pushButton.clicked.connect(zmenaHesla.zmenit_heslo)
    zmenaHesla.lineEdit.returnPressed.connect(zmenaHesla.zmenit_heslo)
    zmenaHesla.pushButton_2.clicked.connect(zmenaHesla.zpetDoAdminPanelu)
    zmenaNazvu.pushButton.clicked.connect(zmenaNazvu.zmenit_nazev)
    zmenaNazvu.lineEdit.returnPressed.connect(zmenaNazvu.zmenit_nazev)
    zmenaNazvu.pushButton_2.clicked.connect(zmenaNazvu.zpet_do_admin_panelu)
    poznamky1.pushButton.clicked.connect(poznamky1.zapsat_do_souboru)
    poznamky1.pushButton_2.clicked.connect(poznamky1.zrusit)
    app.aboutToQuit.connect(hl_menu.ukoncit)
    sys.exit(app.exec_())