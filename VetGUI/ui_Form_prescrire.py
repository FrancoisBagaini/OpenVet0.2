# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Form_prescrire.ui'
#
# Created: Sat Jan  3 22:28:38 2015
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogPrescrire(object):
    def setupUi(self, DialogPrescrire):
        DialogPrescrire.setObjectName("DialogPrescrire")
        DialogPrescrire.resize(409, 532)
        self.widget = QtGui.QWidget(DialogPrescrire)
        self.widget.setGeometry(QtCore.QRect(11, 14, 395, 510))
        self.widget.setObjectName("widget")
        self.MainLayout = QtGui.QVBoxLayout(self.widget)
        self.MainLayout.setObjectName("MainLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit_Prescription = QtGui.QPlainTextEdit(self.widget)
        self.plainTextEdit_Prescription.setMaximumSize(QtCore.QSize(16777215, 80))
        self.plainTextEdit_Prescription.setObjectName("plainTextEdit_Prescription")
        self.verticalLayout.addWidget(self.plainTextEdit_Prescription)
        self.TopLayout = QtGui.QVBoxLayout()
        self.TopLayout.setObjectName("TopLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(120, 0))
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_dose = QtGui.QLineEdit(self.widget)
        self.lineEdit_dose.setMaximumSize(QtCore.QSize(55, 27))
        self.lineEdit_dose.setText("")
        self.lineEdit_dose.setObjectName("lineEdit_dose")
        self.horizontalLayout.addWidget(self.lineEdit_dose)
        self.label_minmax = QtGui.QLabel(self.widget)
        self.label_minmax.setMinimumSize(QtCore.QSize(200, 0))
        self.label_minmax.setObjectName("label_minmax")
        self.horizontalLayout.addWidget(self.label_minmax)
        self.TopLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_frequence = QtGui.QLineEdit(self.widget)
        self.lineEdit_frequence.setObjectName("lineEdit_frequence")
        self.horizontalLayout_4.addWidget(self.lineEdit_frequence)
        self.TopLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_duree = QtGui.QSpinBox(self.widget)
        self.spinBox_duree.setMaximumSize(QtCore.QSize(55, 16777215))
        self.spinBox_duree.setMinimum(1)
        self.spinBox_duree.setObjectName("spinBox_duree")
        self.horizontalLayout_2.addWidget(self.spinBox_duree)
        self.comboBox_duree = QtGui.QComboBox(self.widget)
        self.comboBox_duree.setMinimumSize(QtCore.QSize(200, 27))
        self.comboBox_duree.setMaximumSize(QtCore.QSize(16777215, 27))
        self.comboBox_duree.setObjectName("comboBox_duree")
        self.horizontalLayout_2.addWidget(self.comboBox_duree)
        self.TopLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        self.label_3.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.spinBox_qtdelivree = QtGui.QSpinBox(self.widget)
        self.spinBox_qtdelivree.setMinimum(1)
        self.spinBox_qtdelivree.setObjectName("spinBox_qtdelivree")
        self.horizontalLayout_3.addWidget(self.spinBox_qtdelivree)
        self.label_dureemax = QtGui.QLabel(self.widget)
        self.label_dureemax.setMinimumSize(QtCore.QSize(200, 0))
        self.label_dureemax.setObjectName("label_dureemax")
        self.horizontalLayout_3.addWidget(self.label_dureemax)
        self.TopLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.TopLayout)
        self.ButtonLayout = QtGui.QHBoxLayout()
        self.ButtonLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.ButtonLayout.setObjectName("ButtonLayout")
        self.toolButton_detail = QtGui.QToolButton(self.widget)
        self.toolButton_detail.setMinimumSize(QtCore.QSize(28, 28))
        self.toolButton_detail.setMaximumSize(QtCore.QSize(28, 28))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_detail.setIcon(icon)
        self.toolButton_detail.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_detail.setCheckable(True)
        self.toolButton_detail.setObjectName("toolButton_detail")
        self.ButtonLayout.addWidget(self.toolButton_detail)
        self.toolButton_prescrire = QtGui.QToolButton(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/images/TransfertUp2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_prescrire.setIcon(icon1)
        self.toolButton_prescrire.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_prescrire.setObjectName("toolButton_prescrire")
        self.ButtonLayout.addWidget(self.toolButton_prescrire)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ButtonLayout.addItem(spacerItem)
        self.pushButton_Cancel = QtGui.QPushButton(self.widget)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.ButtonLayout.addWidget(self.pushButton_Cancel)
        self.pushButton_Valid = QtGui.QPushButton(self.widget)
        self.pushButton_Valid.setObjectName("pushButton_Valid")
        self.ButtonLayout.addWidget(self.pushButton_Valid)
        self.verticalLayout.addLayout(self.ButtonLayout)
        self.MainLayout.addLayout(self.verticalLayout)
        self.frame_detail = QtGui.QFrame(self.widget)
        self.frame_detail.setEnabled(True)
        self.frame_detail.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_detail.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_detail.setObjectName("frame_detail")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_detail)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit_info = QtGui.QPlainTextEdit(self.frame_detail)
        self.plainTextEdit_info.setMaximumSize(QtCore.QSize(16777215, 80))
        self.plainTextEdit_info.setReadOnly(True)
        self.plainTextEdit_info.setObjectName("plainTextEdit_info")
        self.verticalLayout_2.addWidget(self.plainTextEdit_info)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtGui.QLabel(self.frame_detail)
        self.label_5.setMinimumSize(QtCore.QSize(100, 0))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_Posologie = QtGui.QLineEdit(self.frame_detail)
        self.lineEdit_Posologie.setObjectName("lineEdit_Posologie")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_Posologie)
        self.label_6 = QtGui.QLabel(self.frame_detail)
        self.label_6.setMinimumSize(QtCore.QSize(100, 0))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_Composition = QtGui.QLineEdit(self.frame_detail)
        self.lineEdit_Composition.setObjectName("lineEdit_Composition")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_Composition)
        self.label_7 = QtGui.QLabel(self.frame_detail)
        self.label_7.setMinimumSize(QtCore.QSize(100, 0))
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_Dose2 = QtGui.QLineEdit(self.frame_detail)
        self.lineEdit_Dose2.setReadOnly(True)
        self.lineEdit_Dose2.setObjectName("lineEdit_Dose2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_Dose2)
        self.label_8 = QtGui.QLabel(self.frame_detail)
        self.label_8.setMinimumSize(QtCore.QSize(100, 0))
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.comboBox_Galenique = QtGui.QComboBox(self.frame_detail)
        self.comboBox_Galenique.setMaximumSize(QtCore.QSize(16777215, 27))
        self.comboBox_Galenique.setObjectName("comboBox_Galenique")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBox_Galenique)
        self.horizontalLayout_5.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(108, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.MainLayout.addWidget(self.frame_detail)

        self.retranslateUi(DialogPrescrire)
        QtCore.QMetaObject.connectSlotsByName(DialogPrescrire)

    def retranslateUi(self, DialogPrescrire):
        DialogPrescrire.setWindowTitle(QtGui.QApplication.translate("DialogPrescrire", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogPrescrire", "Dose :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_minmax.setText(QtGui.QApplication.translate("DialogPrescrire", "dose", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DialogPrescrire", "Fréquence :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogPrescrire", "Durée :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogPrescrire", "Unitées délivrées :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_dureemax.setText(QtGui.QApplication.translate("DialogPrescrire", "duree_max", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_detail.setToolTip(QtGui.QApplication.translate("DialogPrescrire", "Affiche détail des données pharmaceutiques", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_detail.setText(QtGui.QApplication.translate("DialogPrescrire", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_prescrire.setToolTip(QtGui.QApplication.translate("DialogPrescrire", "Insérer dans la préscription", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_prescrire.setText(QtGui.QApplication.translate("DialogPrescrire", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("DialogPrescrire", "Annuler", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Valid.setText(QtGui.QApplication.translate("DialogPrescrire", "Valider", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("DialogPrescrire", "Posologie: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("DialogPrescrire", "Composition: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("DialogPrescrire", "Dose: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("DialogPrescrire", "Galénique :", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
