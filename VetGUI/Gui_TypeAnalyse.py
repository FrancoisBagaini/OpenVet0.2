#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_DialogTypeAnalyse import Ui_DialogTypeAnalyse
from Core_Analyse import TypeAnalyse

class FormTypeAnalyse(QDialog, Ui_DialogTypeAnalyse):
    def __init__(self,idTypeAnalyse,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_main)
        self.MyTypeAnalyse=TypeAnalyse(idTypeAnalyse)
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyTypeAnalyse)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.lineEdit_Libele, 1)
        self.mapper.addMapping(self.plainTextEdit_Remarque, 2)
        self.mapper.addMapping(self.checkBox_isImage, 3)
        self.mapper.toFirst()
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        self.pushButton_Delete.clicked.connect(self.OnDelete)
        self.pushButton_Valid.clicked.connect(self.OnValid)
        self.pushButton_Add.clicked.connect(self.OnNew)
         
    def OnDelete(self):
        if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de vouloir effacer ce type d\'analyse?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.Yes:
            self.MyTypeAnalyse.Delete(self.mapper.currentIndex())
            self.mapper.submit()
            self.accept()
     
    def OnValid(self):
        if self.lineEdit_Libele.text().isEmpty():
            QMessageBox.warning(self,u"Alerte OpenVet",'Le champ Type d\'analyse n\'est pas renseigné', QMessageBox.Ok | QMessageBox.Default)
            return
        if self.plainTextEdit_Remarque.toPlainText().length()>200:
            QMessageBox.warning(self,u"Alerte OpenVet",'Le champ Remarque est trop long : %s pour 200 caractères maxi'%self.plainTextEdit_Remarque.toPlainText().length(), QMessageBox.Ok | QMessageBox.Default)
            return
        if self.mapper.submit():
            self.MyTypeAnalyse.Update(self.mapper.currentIndex())
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Ce type d\'analyse est déjà présent', QMessageBox.Ok | QMessageBox.Default)
             
    def OnNew(self):
        self.MyTypeAnalyse.New()
        self.mapper.toFirst()
    
    def OnCancel(self):
        self.close()