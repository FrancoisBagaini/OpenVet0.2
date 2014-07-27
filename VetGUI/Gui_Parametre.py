#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_DialogParametre import Ui_DialogParametre
from Core_Analyse import Parametre
from Gui_Unite import FormUnite

class FormParametreAnalyse(QDialog, Ui_DialogParametre):
    def __init__(self,Parametre,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_Main)
        self.MyParametre=Parametre
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(Parametre)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.lineEdit_Nom, 3)
        self.mapper.addMapping(self.lineEdit_Remarque, 8)
        self.mapper.addMapping(self.checkBox_isQuantitatif, 4)     
        self.mapper.addMapping(self.lineEdit_NormMin, 6)
        self.mapper.addMapping(self.lineEdit_NormMax, 7)       
        self.comboBox_Unite.setModel(Parametre.relationModel(5))
        self.comboBox_Unite.setModelColumn(Parametre.relationModel(5).fieldIndex('Unite'))
        self.mapper.addMapping(self.comboBox_Unite, 5)
        self.mapper.toFirst()
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        self.pushButton_Delete.clicked.connect(self.OnDelete)
        self.pushButton_Valid.clicked.connect(self.OnValid)
        self.pushButton_Add.clicked.connect(self.OnNew)
        self.toolButton_Unite.clicked.connect(self.OnUnite)
        self.connect(self.checkBox_isQuantitatif,SIGNAL("stateChanged(int)"),self.OncheckBox)
    
    def OncheckBox(self,state):
        if state==0:
            self.comboBox_Unite.setVisible(False)
            self.lineEdit_NormMin.setVisible(False)
            self.lineEdit_NormMax.setVisible(False)
            self.label_Unite.setVisible(False)
            self.label_Max.setVisible(False)
            self.label_Min.setVisible(False)
            self.label_Norme.setVisible(False)
        if state==2:
            self.comboBox_Unite.setVisible(True)
            self.lineEdit_NormMin.setVisible(True)
            self.lineEdit_NormMax.setVisible(True)
            self.label_Unite.setVisible(True)
            self.label_Max.setVisible(True)
            self.label_Min.setVisible(True)
            self.label_Norme.setVisible(True)
        
    def OnDelete(self):
        self.MyParametre.Delete(self.mapper.currentIndex())
        self.mapper.submit()
        self.accept()
    
    def OnValid(self):
        if self.lineEdit_Nom.text().isEmpty():
            print 'erreur'
        if self.checkBox_isQuantitatif.isChecked():
            pass
        self.mapper.submit()
        self.MyParametre.Update(self.mapper.currentIndex())
        self.accept()
        
    def OnNew(self):
        self.MyParametre.New()
        self.mapper.toFirst()
    
    def OnCancel(self):
        self.close()
        
    def OnUnite(self):
        MyFormUnite=FormUnite(self.comboBox_Unite.currentText(),True)
        if MyFormUnite.exec_():
            #TODO: maj self.comboBox_Unite
            pass
        
