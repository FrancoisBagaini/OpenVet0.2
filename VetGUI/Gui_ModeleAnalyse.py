#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PySide import QtCore, QtGui
sys.path.append('../VetCore')
from ui_Form_DialogModeleAnalyse import Ui_DialogModelAnalyse
from Core_Analyse import ModelesAnalyse

class FormModeleAnalyse(QDialog, Ui_DialogModelAnalyse):
    def __init__(self, Modele,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_ModeleAnalyse)
        #TODO mapper?
        self.lineEdit_ModeleLibele.setText(Modele.Modele[3])
        self.plainTextEdit_RemarqueModel.setPlainText(Modele.Modele[5])
        self.horizontalSlider_Modele.setValue(Modele.Modele[6])
        self.listWidget_Parametres.clear()
        for i in Modele.Resultat:   #Paramètre
            self.listWidget_Parametres.addItem(i[1].toString())
        self.MyModels=ModelesAnalyse(Modele.Modele[2],Modele.Modele[4])
        self.MyModels.selection=Modele.Modele[1]
        self.MyModel=Modele
        if Modele.Modele[0]==0:
            self.MyModels.insertRows(Modele.Modele)
        self.horizontalSlider_Modele.setMinimum(0)
        self.horizontalSlider_Modele.setMaximum(self.MyModels.rowCount())
        self.listView_Modeles.setModel(self.MyModels)
        self.connect(self.horizontalSlider_Modele,SIGNAL('valueChanged(int)'),self.OnSlider)
        self.plainTextEdit_RemarqueModel.textChanged.connect(self.OnRemarque)
        
    def OnSlider(self,value):
        self.MyModel.Modele[6]=value
        self.MyModels.setData(self.MyModels.indexSelection, value, Qt.EditRole)
        self.MyModels.sort(3,Qt.AscendingOrder)
#        self.Print()

    def OnRemarque(self):
        self.MyModel.Modele[5]=self.plainTextEdit_RemarqueModel.toPlainText()
        
    def Print(self):    #debug Only
        for i in self.MyModels.listdata:
            tmp=[]
            for j in i:
                try:
                    tmp.append('%s'%j.toString())
                except:
                    tmp.append('%s'%j) 
            print ';'.join(tmp)   