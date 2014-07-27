#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_DialogUnite import Ui_DialogUnite


class Unite(QSqlTableModel):
    def __init__(self, NameUnite,isConcentration,parent=None, *args):
        QSqlTableModel.__init__(self, parent, *args)
        self.isConcentration=isConcentration
        self.setTable('Unite')
        self.setFilter('Unite=\"%s\"' % NameUnite)
        self.select()
#        print self.rowCount()
    
    def New(self):
        self.setFilter('idUnite=0')
        self.insertRow(0)
        self.setData(self.index(0, 0), QVariant(0), Qt.EditRole)
        self.setData(self.index(0, 1), QVariant(""), Qt.EditRole)
        self.setData(self.index(0, 2), QVariant(self.isConcentration), Qt.EditRole)
        self.setData(self.index(0, 3), QVariant(True), Qt.EditRole)
        
    def Delete(self,row):
        if not self.removeRow(row):
            self.setData(self.index(row,3), QVariant(False),Qt.EditRole)    #isActif=False si l'intégrité référentielle n'est pas respectée
        self.submitAll()
        
    def Update(self,index):
        self.submitAll()


class FormUnite(QDialog, Ui_DialogUnite):
    def __init__(self,NameUnite,isConcentration,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout)
        self.isConcentration=isConcentration
        self.MyUnite=Unite(NameUnite,isConcentration)
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyUnite)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.lineEdit_Unite, 1)
        self.mapper.addMapping(self.checkBox_isConcentration, 2)
        self.mapper.toFirst()
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        self.pushButton_Delete.clicked.connect(self.OnDelete)
        self.pushButton_Valid.clicked.connect(self.OnValid)
        self.pushButton_Add.clicked.connect(self.OnNew)
        
    def OnDelete(self):
        if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de vouloir effacer cette unité?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.Yes:
            self.MyUnite.Delete(self.mapper.currentIndex())
            self.mapper.submit()
            self.accept()
    
    def OnValid(self):
        if self.lineEdit_Unite.text().isEmpty():
            QMessageBox.warning(self,u"Alerte OpenVet",'Le champ Unité n\'est pas renseigné', QMessageBox.Ok | QMessageBox.Default)
            return
        if (not self.checkBox_isConcentration.isChecked() and self.isConcentration)==True:
            if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de ne pas attribuer cette unité à une concentration?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.No:
                return
        if self.mapper.submit():
            self.MyUnite.Update(self.mapper.currentIndex())
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Cette Unité est déjà présente dans la table Unite', QMessageBox.Ok | QMessageBox.Default)
            
    def OnNew(self):
        self.MyUnite.New()
        self.mapper.toFirst()
    
    def OnCancel(self):
        self.close()