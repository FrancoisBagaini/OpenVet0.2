# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_DialogAnalyse.ui'
#
# Created: Thu May  8 10:29:29 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form_DialogAnalyse(object):
    def setupUi(self, Form_DialogAnalyse):
        Form_DialogAnalyse.setObjectName("Form_DialogAnalyse")
        Form_DialogAnalyse.resize(711, 477)
        self.layoutWidget = QtGui.QWidget(Form_DialogAnalyse)
        self.layoutWidget.setGeometry(QtCore.QRect(2, 2, 710, 471))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(82, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_Fichier = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Fichier.setObjectName("lineEdit_Fichier")
        self.horizontalLayout.addWidget(self.lineEdit_Fichier)
        self.toolButton_Fichier = QtGui.QToolButton(self.layoutWidget)
        self.toolButton_Fichier.setObjectName("toolButton_Fichier")
        self.horizontalLayout.addWidget(self.toolButton_Fichier)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_FichierInterne = QtGui.QLabel(self.layoutWidget)
        self.label_FichierInterne.setObjectName("label_FichierInterne")
        self.horizontalLayout_5.addWidget(self.label_FichierInterne)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.radioButton_doc = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_doc.setObjectName("radioButton_doc")
        self.horizontalLayout_5.addWidget(self.radioButton_doc)
        self.radioButton_img = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_img.setObjectName("radioButton_img")
        self.horizontalLayout_5.addWidget(self.radioButton_img)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(82, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_Titre = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Titre.setObjectName("lineEdit_Titre")
        self.horizontalLayout_2.addWidget(self.lineEdit_Titre)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.textEdit_DocAnalyse = QtGui.QTextEdit(self.layoutWidget)
        self.textEdit_DocAnalyse.setMinimumSize(QtCore.QSize(260, 320))
        self.textEdit_DocAnalyse.setObjectName("textEdit_DocAnalyse")
        self.horizontalLayout_3.addWidget(self.textEdit_DocAnalyse)
        self.label_ImageViewer = QtGui.QLabel(self.layoutWidget)
        self.label_ImageViewer.setMinimumSize(QtCore.QSize(260, 320))
        self.label_ImageViewer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_ImageViewer.setFrameShape(QtGui.QFrame.Panel)
        self.label_ImageViewer.setText("")
        self.label_ImageViewer.setObjectName("label_ImageViewer")
        self.horizontalLayout_3.addWidget(self.label_ImageViewer)
        spacerItem2 = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.pushButton_Cancel = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_Cancel.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout_4.addWidget(self.pushButton_Cancel)
        self.pushButton_Ok = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_Ok.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton_Ok.setObjectName("pushButton_Ok")
        self.horizontalLayout_4.addWidget(self.pushButton_Ok)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form_DialogAnalyse)
        QtCore.QMetaObject.connectSlotsByName(Form_DialogAnalyse)

    def retranslateUi(self, Form_DialogAnalyse):
        Form_DialogAnalyse.setWindowTitle(QtGui.QApplication.translate("Form_DialogAnalyse", "OpenVet", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Chemin :", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_Fichier.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_FichierInterne.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Nom fichier interne ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_doc.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Document", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_img.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Titre :", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Annuler", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Ok.setText(QtGui.QApplication.translate("Form_DialogAnalyse", "Valider", None, QtGui.QApplication.UnicodeUTF8))

