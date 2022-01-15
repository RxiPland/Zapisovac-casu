from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox


class Ui_MainWindow_poznamky_okno(object):

    def center(self):

        # funkce, která přesune okno programu do prostřed obrazovky

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    def setupUi(self, MainWindow):
        
        MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(525, 370)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 24, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 481, 231))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlaceholderText("zde napište svoje poznámky")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 300, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 300, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")


        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 300, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_3.clicked.connect(self.plainTextEdit.clear)


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Poznámky"))
        self.label.setText(_translate("MainWindow", "Vaše poznámky:"))
        self.pushButton.setText(_translate("MainWindow", "Uložit a odejít"))
        self.pushButton_2.setText(_translate("MainWindow", "Zrušit"))
        self.pushButton_3.setText(_translate("MainWindow", "Vymazat"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_poznamky_okno()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
