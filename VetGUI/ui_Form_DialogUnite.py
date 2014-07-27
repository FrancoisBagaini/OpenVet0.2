# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogUnite.ui'
#
# Created: Sat Jun 14 10:15:46 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogUnite(object):
    def setupUi(self, DialogUnite):
        DialogUnite.setObjectName("DialogUnite")
        DialogUnite.resize(382, 99)
        self.layoutWidget = QtGui.QWidget(DialogUnite)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 364, 66))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 27))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_Unite = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Unite.setMinimumSize(QtCore.QSize(0, 27))
        self.lineEdit_Unite.setText("")
        self.lineEdit_Unite.setMaxLength(20)
        self.lineEdit_Unite.setObjectName("lineEdit_Unite")
        self.horizontalLayout.addWidget(self.lineEdit_Unite)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox_isConcentration = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_isConcentration.setObjectName("checkBox_isConcentration")
        self.horizontalLayout.addWidget(self.checkBox_isConcentration)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_Cancel = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_Cancel.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout_5.addWidget(self.pushButton_Cancel)
        self.pushButton_Add = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_Add.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton_Add.setObjectName("pushButton_Add")
        self.horizontalLayout_5.addWidget(self.pushButton_Add)
        self.pushButton_Delete = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_Delete.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton_Delete.setObjectName("pushButton_Delete")
        self.horizontalLayout_5.addWidget(self.pushButton_Delete)
        self.pushButton_Valid = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_Valid.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton_Valid.setObjectName("pushButton_Valid")
        self.horizontalLayout_5.addWidget(self.pushButton_Valid)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(DialogUnite)
        QtCore.QMetaObject.connectSlotsByName(DialogUnite)

    def retranslateUi(self, DialogUnite):
        DialogUnite.setWindowTitle(QtGui.QApplication.translate("DialogUnite", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogUnite", "Unité :", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_isConcentration.setText(QtGui.QApplication.translate("DialogUnite", "Concentration", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("DialogUnite", "Annuler", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Add.setText(QtGui.QApplication.translate("DialogUnite", "Nouveau", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Delete.setText(QtGui.QApplication.translate("DialogUnite", "Supprimer", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Valid.setText(QtGui.QApplication.translate("DialogUnite", "Valider", None, QtGui.QApplication.UnicodeUTF8))

