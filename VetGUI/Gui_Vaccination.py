#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4 import QtCore, QtGui
import sys
import time

from Core_Vaccination import *
from MyGenerics import *


#from PySide import QtCore, QtGui
#sys.path.append('../VetCore')
class GuiVaccination():
    
    def __init__(self,parent=None):
        self.parent=parent
        self.parent.plainTextEdit_remarque.SetMaxLength(200)
        now=QDate.currentDate()
        self.parent.dateEdit_dateVaccination.setDate(now)
        self.parent.lineEdit_denomination.setEnabled(False)
        self.parent.lineEdit_laboratoire.setEnabled(False)
        self.parent.lineEdit_NoLot.setEnabled(False)
        self.parent.dateEdit_datePeremption.setEnabled(False)
        self.parent.comboBox_periodeRappel.setModel(MyComboModel(self.parent,'GetPeriodes'))
        
        self.PopMenus=[]
        for i in [self.parent.tableView_Vaccins,self.parent.listView_Lot,self.parent.listView_Rappels]:
            i.setContextMenuPolicy(Qt.CustomContextMenu)
            self.parent.connect(i,SIGNAL('customContextMenuRequested(const QPoint&)'), self.OnListViewMenu)
            menu = QMenu(i)
            if i==self.parent.tableView_Vaccins:
                action1=menu.addAction('Editer')
            else:
                action1=menu.addAction('Supprimer')
            action1.setData(i)
            if i==self.parent.tableView_Vaccins:
                self.parent.connect(action1,SIGNAL("triggered()"),self.OnEditVaccin)
            if i==self.parent.listView_Lot:
                self.parent.connect(action1,SIGNAL("triggered()"),self.OnDeleteLot)
            if i==self.parent.listView_Rappels:
                self.parent.connect(action1,SIGNAL("triggered()"),self.OnDeleteRappel)
            self.PopMenus.append(menu)

        #connect actions
        self.parent.comboBox_periodeRappel.currentIndexChanged.connect(self.OnSelectPeriode) 
        self.parent.comboBox_periodeRappel.SetValue(QString(u'Annuel'))
        self.parent.comboBox_valence.currentIndexChanged.connect(self.OnSelectValence)
        self.parent.comboBox_lot.currentIndexChanged.connect(self.OnSelectLot)
        self.parent.toolButton_editValence.clicked.connect(self.OnEditValence)
        self.parent.toolButton_editLot.clicked.connect(self.OnEditLot)
        self.parent.pushButton_ajouterLot.clicked.connect(self.OnAjouterLot)
        self.parent.button_ajouterRelance.clicked.connect(self.OnAjouterRelance)
        self.parent.button_resetVaccin.clicked.connect(self.OnInitVaccin)
        self.parent.button_validerVaccin.clicked.connect(self.OnSaveVaccin)
        


    def SetAnimal(self,idEspece,idAnimal):
        self.idEspece=idEspece
        self.idAnimal=idAnimal
        self.parent.tableView_Vaccins.setModel(MyTableModel(self.parent,3,'GetVaccins(%i)'%self.idAnimal))
#        self.parent.tableView_Vaccins.resizeColumnsToContents()
        self.parent.tableView_Vaccins.horizontalHeader().setStretchLastSection(True)
        self.parent.comboBox_valenceRappel.setModel(MyComboModel(self.parent,'GetValences(%i)'%self.idEspece))
        self.parent.comboBox_valence.setModel(MyComboModel(self.parent,'GetValences(%i)'%self.idEspece))
        
        self.MyVaccination= Vaccination(self.idAnimal,0,self.parent)
        self.parent.listView_Lot.setModel(self.MyVaccination.MyLots)
        self.parent.listView_Rappels.setModel(self.MyVaccination.MyRappels)
        
        # GetNewVaccin by defaut
        idValence=self.MyVaccination.GetNewVaccin()
#        idLot=self.MyVaccination.GetLot(idValence)
        if idValence is not None:
            new=[0,self.idAnimal,idValence,QDate.currentDate(),None,True,'']
        else:
            print 'erreur: Absence de valence par défaut'
            new=[0,self.idAnimal,0,QDate.currentDate(),None,True,'']
        if not self.MyVaccination.SetNew(new):
            return
        self.MyVaccination.New()
                
        self.mapper = QDataWidgetMapper(self.parent)
        self.mapper.setOrientation(Qt.Horizontal)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyVaccination)
        #self.MyVaccination.Print()
        self.MyDelegate=GenericDelegate(self.parent)
        for i in range(2,6):
            #print self.MyVaccination.Fields[i].Name
            self.MyDelegate.insertFieldDelegate(i,self.MyVaccination.Fields[i]) 
        self.mapper.setItemDelegate(self.MyDelegate)
        self.mapper.addMapping(self.parent.dateEdit_dateVaccination,3)
        self.mapper.addMapping(self.parent.comboBox_valence,2)
        self.mapper.addMapping(self.parent.plainTextEdit_remarque,4)
        self.mapper.toFirst()

#     def SetVaccin(self,idVaccination):
#         #TODO : connect to edit vaccin
#         self.MyVaccination= Vaccination(self.idAnimal,idVaccination,self.parent)
#         self.parent.listView_Lot.setModel(self.MyVaccination.MyLots)
#         self.parent.listView_Rappels.setModel(self.MyVaccination.MyRappels)
        
    def OnSelectValence(self):
        self.idValence=self.parent.comboBox_valence.Getid()
        self.parent.comboBox_lot.setModel(MyComboModel(self.parent,'GetLots(%i)'%self.idValence))
        self.parent.comboBox_valenceRappel.Setid(self.idValence)

    def OnSelectLot(self):
        self.idLot=self.parent.comboBox_lot.Getid()
        self.MyLot=Lot(self.idLot,self.parent)
        self.parent.lineEdit_denomination.setText(self.MyLot.GetData(2))
        self.parent.lineEdit_laboratoire.setText(self.MyLot.GetData(1))
        self.parent.lineEdit_NoLot.setText(self.MyLot.GetData(3))
        self.parent.dateEdit_datePeremption.setDate(self.MyLot.GetData(4))
           
    def OnSelectPeriode(self):
#        idPeriode=self.parent.comboBox_periodeRappel.Getid()
        unite=self.parent.comboBox_periodeRappel.GetProperty(1).toString()
        duree=self.parent.comboBox_periodeRappel.GetProperty(2).toInt()
        if not duree[1] or unite.isEmpty():
            return
        date=self.parent.dateEdit_dateVaccination.date()
        if unite==QString(u'mois'):
            newdate=date.addMonths(duree[0])
        if unite==QString(u'jour'):
            newdate=date.addDays(duree[0])
        if unite==QString(u'an'):
            newdate=date.addYears(duree[0])    
        self.parent.dateEdit_dateRelance.setDate(newdate)
        
    def OnListViewMenu(self,point):
        for i in self.PopMenus:
            if i.parent()==self.parent.sender():
                i.exec_(i.parent().mapToGlobal(point))
                break
        
    def OnEditVaccin(self):
        index=self.parent.tableView_Vaccins.currentIndex()
        idVaccin=self.parent.tableView_Vaccins.model().data(index,Qt.UserRole).toInt()[0]
        self.MyVaccination.SetVaccin(idVaccin)
        self.mapper.toFirst()
    
    def OnInitVaccin(self):
        self.MyVaccination.SetVaccin(0)
        self.mapper.toFirst()
    
    def OnEditValence(self):
        new=[0,self.idEspece,'',False,None,True,'']
        model=MyModel('Valence',self.idValence,self.parent)
        if not model.SetNew(new):
            return
        data=[[u'Libelé',1,30],[u'Choix par défaut',2],[u'Remarque',3,200,80],[u'Actif',2]]
        form=MyForm('Edition des Valences vaccinales',data,self.parent)
        form.SetModel(model,{0:2,1:3,2:4,3:5})
        if form.exec_():
            print model.lastid.toInt()[0]
            self.parent.comboBox_valence.setModel(MyComboModel(self.parent,'GetValences(%i)'%self.idEspece))
            self.parent.comboBox_valenceRappel.setModel(MyComboModel(self.parent,'GetValences(%i)'%self.idEspece))
            if model.lastid.toInt()[1]:
                self.parent.comboBox_valence.Setid(model.lastid.toInt()[0])
        
    def OnEditLot(self):
        new=[0,self.idValence,self.MyLot.GetData(5),self.MyLot.GetData(2),None,None,0,50,QDate.currentDate(),QDate.currentDate(),None,True]
        model=MyModel('LotVaccin',self.idLot,self.parent)
        if not model.SetNew(new):
            return
        data=[[u'Laboratoire',4,None,None,u'Editer les fournisseurs'],[u'Dénomination',1,60],[u'Numéro de lot',1,20],[u'Date de péremption',10],[u'Quantité utilisée',8],
              [u'Quantité totale',8],[u'Date d\'ouverture',10],[u'Dernière utilisation',10],[u'Remarque',3,200,80]]
        form=FormLot(data,self.parent)
        form.SetModel(model,{0:2,1:3,2:4,3:5,4:6,5:7,6:8,7:9,8:10})
        if form.exec_():
            print model.lastid.toInt()[0]
            self.parent.comboBox_lot.setModel(MyComboModel(self.parent,'GetLots(%i)'%self.idValence))
            if model.lastid.toInt()[1]:
                print model.lastid.toInt()
                self.parent.comboBox_lot.Setid(model.lastid.toInt()[0])
                
    def OnAjouterLot(self):
        data=self.MyLot.GetNewLine()
        self.parent.listView_Lot.model().NewLine(data)
            
    def OnDeleteLot(self):
        index=self.parent.listView_Lot.currentIndex()
        self.parent.listView_Lot.model().DeleteLine_hard(index.row())
    
    def OnAjouterRelance(self):
        data=[0,u'%s : %s'%(self.parent.dateEdit_dateRelance.date().toString('dd/MM/yyyy'),self.parent.comboBox_valenceRappel.currentText()),self.parent.lineEdit_RemarqueRappel.text(),
              0,0,self.parent.dateEdit_dateRelance.date(),self.parent.comboBox_valenceRappel.Getid()]
        self.parent.listView_Rappels.model().NewLine(data)   
    
    def OnDeleteRappel(self):
        index=self.parent.listView_Rappels.currentIndex()
        self.parent.listView_Rappels.model().DeleteLine_hard(index.row())
        
    def OnSaveVaccin(self):
        pass