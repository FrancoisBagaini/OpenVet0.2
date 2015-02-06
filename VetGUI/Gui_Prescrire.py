#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_prescrire import Ui_DialogPrescrire
from MyGenerics import *

class FormPrescrire(QDialog, Ui_DialogPrescrire):
    def __init__(self, data,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.data=data
        self.prescription=None
        self.label_minmax.setText(data[0])
        self.label_dureemax.setText(data[1])
        self.lineEdit_frequence.setText(data[4])
        self.plainTextEdit_Prescription.setToolTip(data[5])
        self.plainTextEdit_info.setPlainText(data[3])
        self.setLayout(self.MainLayout)
        self.MainLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.fullsize=self.size()
        self.frame_detail.hide()
        self.resize(QSize(self.fullsize.width(),self.fullsize.height()-210))
        self.comboBox_duree.setModel(MyComboModel(self,'GetUnites_ForType(\'Temps\')'))
        self.comboBox_Galenique.setModel(MyComboModel(self,'GetUnites_ForType(\'Galen\')'))
        self.lineEdit_Posologie.setText('*%.2f'%self.data[8])
        self.lineEdit_Posologie.setToolTip('Pour %.2f Kg'%self.data[8])
        self.pushButton_Valid.setAutoDefault(False)
        self.toolButton_detail.toggled.connect(self.ShowDetail)
        self.toolButton_prescrire.clicked.connect(self.FillPrescription)
        self.lineEdit_Posologie.textChanged.connect(self.CalculDose)
        self.lineEdit_Composition.textChanged.connect(self.CalculDose)
        self.pushButton_Valid.clicked.connect(self.OnValid)
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        
    def ShowDetail(self):
        if self.frame_detail.isVisible():
            self.frame_detail.hide()
            self.resize(QSize(self.fullsize.width(),self.fullsize.height()-210))
        else:
            self.frame_detail.setVisible(True)
            self.resize(self.fullsize)
            self.lineEdit_Posologie.setFocus()
            self.lineEdit_Posologie.setCursorPosition(0)
            
    def FillPrescription(self):
        text='%s:\n%s %s'%(self.data[6],self.lineEdit_dose.text(),self.data[2])
        if eval(str(self.lineEdit_dose.text()).replace('/','.0/'))>1:
            text=text+'s'
        text=text+', par voie %s, %s pendant %s %s'%(self.data[7],self.lineEdit_frequence.text(),self.spinBox_duree.text(),self.comboBox_duree.currentText())
        if eval(str(self.spinBox_duree.text()))>1 and self.comboBox_duree.currentText()!='mois':
            text=text+'s.'
        else:
            text=text+'.'
        self.plainTextEdit_Prescription.setPlainText(text)

    def CalculDose(self):
        try:
            poso=eval(str(self.lineEdit_Posologie.text()))
            compo=eval(str(self.lineEdit_Composition.text()))
            self.lineEdit_Dose2.setText(QString(str(float(poso)/compo)))
        except:
            return
    
    def OnValid(self):
        if self.plainTextEdit_Prescription.toPlainText().isEmpty():
            MyError(self,u'La préscription est vide')
        else:
            self.prescription=self.plainTextEdit_Prescription.toPlainText()
            self.dose=eval(str(self.lineEdit_dose.text()).replace('/','.0/'))
            self.duree=eval(str(self.spinBox_duree.text()))
#            self.idtemps=self.comboBox_duree.itemData(self.comboBox_duree.currentIndex(), Qt.UserRole).toInt()[0]
            self.idtemps=self.comboBox_duree.Getid()
            self.delivre=eval(str(self.spinBox_qtdelivree.text()))
            self.remarque=self.lineEdit_Remarque.text()
            self.accept()
    
    def OnCancel(self):
        self.reject()