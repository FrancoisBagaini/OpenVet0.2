# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogModeleAnalyse.ui'
#
# Created: Tue May 20 11:32:17 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogModelAnalyse(object):
    def setupUi(self, DialogModelAnalyse):
        DialogModelAnalyse.setObjectName("DialogModelAnalyse")
        DialogModelAnalyse.resize(366, 445)
        self.widget = QtGui.QWidget(DialogModelAnalyse)
        self.widget.setGeometry(QtCore.QRect(11, 12, 344, 421))
        self.widget.setObjectName("widget")
        self.verticalLayout_ModeleAnalyse = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_ModeleAnalyse.setObjectName("verticalLayout_ModeleAnalyse")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_ModelLibele = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        self.label_ModelLibele.setFont(font)
        self.label_ModelLibele.setObjectName("label_ModelLibele")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_ModelLibele)
        self.lineEdit_ModeleLibele = QtGui.QLineEdit(self.widget)
        self.lineEdit_ModeleLibele.setReadOnly(True)
        self.lineEdit_ModeleLibele.setObjectName("lineEdit_ModeleLibele")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_ModeleLibele)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.listWidget_Parametres = QtGui.QListWidget(self.widget)
        self.listWidget_Parametres.setObjectName("listWidget_Parametres")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.listWidget_Parametres)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.plainTextEdit_RemarqueModel = QtGui.QPlainTextEdit(self.widget)
        self.plainTextEdit_RemarqueModel.setMaximumSize(QtCore.QSize(16777215, 58))
        self.plainTextEdit_RemarqueModel.setObjectName("plainTextEdit_RemarqueModel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.plainTextEdit_RemarqueModel)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalSlider_Modele = QtGui.QSlider(self.widget)
        self.horizontalSlider_Modele.setMinimum(1)
        self.horizontalSlider_Modele.setMaximum(20)
        self.horizontalSlider_Modele.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Modele.setObjectName("horizontalSlider_Modele")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.horizontalSlider_Modele)
        self.verticalLayout_ModeleAnalyse.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.listView_Modeles = QtGui.QListView(self.widget)
        self.listView_Modeles.setObjectName("listView_Modeles")
        self.horizontalLayout.addWidget(self.listView_Modeles)
        self.verticalLayout_ModeleAnalyse.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_ModeleAnalyse.addWidget(self.buttonBox)
        self.label_ModelLibele.setBuddy(self.lineEdit_ModeleLibele)
        self.label.setBuddy(self.listWidget_Parametres)
        self.label_2.setBuddy(self.plainTextEdit_RemarqueModel)
        self.label_3.setBuddy(self.horizontalSlider_Modele)

        self.retranslateUi(DialogModelAnalyse)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogModelAnalyse.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogModelAnalyse.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModelAnalyse)

    def retranslateUi(self, DialogModelAnalyse):
        DialogModelAnalyse.setWindowTitle(QtGui.QApplication.translate("DialogModelAnalyse", "OpenVet", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ModelLibele.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Modèle :", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Paramètres:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Remarque :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogModelAnalyse", "Priorité :", None, QtGui.QApplication.UnicodeUTF8))

