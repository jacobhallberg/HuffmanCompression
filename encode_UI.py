# Author: Jacob Hallberg
# Last Edited: 12/25/2017
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HuffmanEncode(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(772, 832)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 9, 771, 832))

        font = QtGui.QFont()
        font.setFamily("Garuda")
        font.setPointSize(14)

        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        self.Encode = QtWidgets.QWidget()
        self.Encode.setObjectName("Encode")

        self.UploadFile = QtWidgets.QPushButton(self.Encode)
        self.UploadFile.setGeometry(QtCore.QRect(170, 580, 411, 141))
        self.UploadFile.setObjectName("Upload File")

        self.label_2 = QtWidgets.QLabel(self.Encode)
        self.label_2.setGeometry(QtCore.QRect(70, 535, 611, 35))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.tabWidget.addTab(self.Encode, "")

        self.Decode = QtWidgets.QWidget()
        self.Decode.setObjectName("Decode")

        self.DecodeFile = QtWidgets.QPushButton(self.Decode)
        self.DecodeFile.setGeometry(QtCore.QRect(170, 580, 411, 141))
        self.DecodeFile.setObjectName("Decode File")

        self.label = QtWidgets.QLabel(self.Decode)
        self.label.setGeometry(QtCore.QRect(70, 535, 611, 35))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.textBrowser = QtWidgets.QTextBrowser(self.Decode)
        self.textBrowser.setGeometry(QtCore.QRect(0, 10, 780, 521))
        self.textBrowser.setObjectName("textBrowser")

        self.tabWidget.addTab(self.Decode, "")

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Huffamn Encoding - Jacob Hallberg"))
        self.UploadFile.setText(_translate("MainWindow", "Click to Browse Files"))
        self.label_2.setText(_translate("MainWindow", "Click below to get started"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Encode), _translate("MainWindow", "Encode File"))
        self.DecodeFile.setText(_translate("MainWindow", "Click to Browse Files"))
        self.label.setText(_translate("MainWindow", "Upload Compressed File, Code Book"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Decode), _translate("MainWindow", "Decode File"))

