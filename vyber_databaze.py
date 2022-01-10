from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
import os

class Ui_MainWindow_Vyber_db(object):

    def center(self):

        # funkce, která přesune okno programu do prostřed obrazovky

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def pridat_policka(self, a):

        # přidá prázdná políčka do boxu v okně: "výběr projektu"

        global vsechny_db_list

        vsechny_db_list = []

        cesta1 = os.getcwd()

        soubory = os.listdir(cesta1)

        for soubor in soubory:

            if ".db" in soubor:
                
                soubor = soubor.replace(".db", "")
                vsechny_db_list.append(soubor)

        if len(vsechny_db_list) == 0:

            return "ZADNE_DB_K_DISPOZICI"

        else:

        
            if a == "nepridavat":

                pass

            else:

                for i in range(len(vsechny_db_list)):
                
                    self.comboBox.addItem("")


    def dosadit_nazev_do_boxu(self):

        # dosadí názvy do předpřipravených polí boxu v okně: "výběr projektu"

        pocitadlo2 = int(0)

        for nazev_db in vsechny_db_list:

            self.comboBox.setItemText(pocitadlo2, nazev_db)

            pocitadlo2 += 1


    def setupUi(self, MainWindow):


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 190)

        MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(42, 84, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 541, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(292, 113, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")


        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 110, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.pridat_policka("")
        self.comboBox.setEditable(False)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 110, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):


        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Výběr projektu"))
        self.label.setText(_translate("MainWindow", "Vybrat existující:"))
        self.label_2.setText(_translate("MainWindow", "Vyberte projekt, ke kterému chcete zapisovat časy:"))
        self.pushButton.setText(_translate("MainWindow", "Vytvořit nový"))
        self.label_3.setText(_translate("MainWindow", "nebo"))
        self.dosadit_nazev_do_boxu()
