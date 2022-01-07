# Udělal RxiPland

from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QMainWindow, QApplication
from PyQt5.QtWidgets import QMessageBox
from vyber_databaze import Ui_MainWindow_Vyber_db
from vytvorit_novou_db import Ui_MainWindow_Vytvorit_novou_databazi

class vybrani_databaze(QMainWindow, Ui_MainWindow_Vyber_db):

    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


    def tlacitko_zpet(self):

        # tlačítko zpět v přidat nový projekt

        vytvorit_novou.close()
        self.pridat_policka("nepridavat")
        self.dosadit_nazev_do_boxu()
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

   

class vytvorit_databazi(QMainWindow, Ui_MainWindow_Vytvorit_novou_databazi):

    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)



    def otevrit_okno(self):
        
        vyber_db1.close()
        vyber_db1.center()
        vytvorit_novou.center()
        vytvorit_novou.show()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    vyber_db1 = vybrani_databaze()
    vytvorit_novou = vytvorit_databazi()
    vyber_db1.pro_zacatek()
    vyber_db1.pushButton.clicked.connect(vytvorit_novou.otevrit_okno)
    vytvorit_novou.pushButton_2.clicked.connect(vyber_db1.tlacitko_zpet)
    sys.exit(app.exec_())