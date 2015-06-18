#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui,QtSql
#from PySide import QtCore, QtGui
import config
from ui_Form_openvet import Ui_MainWindow
from Gui_Medical import TabMedical

from MyGenerics import *
from Core_Animal import *

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, db,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.db=db
        self.editConsultation = TabMedical(db,self)
        Fiches_Layout=QVBoxLayout()
        Fiches_Layout.addWidget(self.tabWidget_fiches)
        Fiches_Layout.addWidget(self.editConsultation)
        self.centralwidget.setLayout(Fiches_Layout)
        
        #En attendant la connection avec la gestion client
        self.editConsultation.setVisible(False)
        self.idClient=None
        self.idAnimal=None
        self.MyAnimal=None
        
        self.OnSelectClient()
        
        #Connect actions
        self.comboBox_Animal.currentIndexChanged.connect(self.OnSelectAnimal)
        self.toolButton_editAnimal.clicked.connect(self.OnEditAnimal)
        self.toolButton_Poids.clicked.connect(self.OnMesuresAnimal)
        self.toolButton_Relance.clicked.connect(self.OnRelancesAnimal)
        self.actionQuitter.triggered.connect(self.Mycloseapp)
    
    def OnSelectClient(self):
        self.idClient=4 #TODO =Comobo.id
        self.comboBox_Animal.setModel(MyComboModel(self,'GetAnimals(%i)'%self.idClient))
        self.OnSelectAnimal()
        
    def OnSelectAnimal(self):
        self.idAnimal=self.comboBox_Animal.Getid()
        self.idEspece=self.comboBox_Animal.GetProperty(1).toInt()[0]
        self.MyAnimal=Animal('Animal',self.idAnimal,self)
        self.editConsultation.SelectAnimal(self.idEspece,self.idAnimal)
        self.textBrowser_animal.setText(self.MyAnimal.GetAbstract())
        self.textBrowser_animal.setToolTip(self.MyAnimal.Abstract[1].toString())
    
    def OnEditAnimal(self):
        new=[0,'',0,0,False,'','',None,0,None,'',True,False,False,True,'']#date par défaut
        model=MyModel('Animal',self.idAnimal,self)
        if not model.SetNew(new):
            return
        data=[[u'Nom',1,60],[u'Espèce',4,None,None,u'Editer les unités espèces'],[u'Race',4,None,None,u'Editer les races'],[u'Croisement',2],[u'robe',4],[u'Sexe',4],
              [u'Date de naissance',10],[u'Stérilisation',2],[u'Identification',1,14],[u'Remarque',3,200,80],[u'Relances',2],[u'Perdu',2],[u'Décès',2]]
        form=FormAnimal(self.idEspece,data,self)
        form.SetMyModel(model,{0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12,12:13})
        if form.exec_():
            self.OnSelectAnimal()

    def OnMesuresAnimal(self):
        new=[0,self.idAnimal,QDate.currentDate(),0.0,0.0,0.0,None,None,True,'']
        idMesure=self.MyAnimal.GetLastMesure()
        model=MyModel('PoidsMesure',idMesure,self)
        if not model.SetNew(new):
            return
        data=[['',11,None,None,None,2],[u'Date',10],[u'Poids',1,6],[u'Taille au garrot',1,6],[u'Tour de Thorax',1,6],[u'Photo',1,80,None,u'Parcourir'],
              [u'Remarque',3,200,80]]
        form=FormMesures(self.MyAnimal.idAnimal,data,self)
#        form.SetMyModel(model,{1:2,2:3,3:4,4:5,5:6,6:7,7:8})
        form.SetModel(model,{1:2,2:3,3:4,4:5,5:6,6:7,7:8})
        if form.exec_():
            self.OnSelectAnimal()
    
    def OnRelancesAnimal(self):
        new=[0,self.idAnimal,1,QDate.currentDate(),None,True,'']
        idRelance=self.MyAnimal.GetLastRelance()
        model=MyModel('Relance',idRelance,self)
        if not model.SetNew(new):
            return
        data=[['',5,None,60,None,2],[u'Date',10],[u'Type de Relance',4,None,None,u'Editer les types de relance'],[u'Mode de Relance',5,None,60],[u'Remarque',3,200,80],
              [u'Relance active',2]]
        form=FormRelances(self.MyAnimal.idAnimal,self.idClient,data,self)
        form.SetMyModel(model,{1:3,2:2,4:4,5:5})
        if form.exec_():
            self.OnSelectAnimal()
         
    def Mycloseapp(self):
        self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #Test
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName ( config.host )
    db.setUserName ( config.user )
    db.setPassword ( config.password )
    db.setDatabaseName(config.database)
    if not db.open():
        QtGui.QMessageBox.warning(None, "OpenVet",QtCore.QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)
    #end test
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())
