#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui
#sys.path.append('../VetCore')
from Gui_Pathologie import FormPathologie

import time
import Tables
import config
import Core_Pathologie
import Core_Critere
from MyGenerics import *
from Core_Consultation import *


class GuiConsultation():
    idConsultation=0
    NewConsultation=True
    
    def __init__(self,parent=None):
        self.Qbase=parent.Qbase
        self.DBase=Tables.DataBase(config.database) # TODO: remove line
        self.parent=parent
#        self.editPathologie=None
        self.MyConsult= Consultation(self.DBase,0)                   #TODO: use QBase or Request and move to one consultation 
        self.MyPathologie=Core_Pathologie.Pathologie(self.DBase)     #TODO: use QBase or Request
        #        a=MyComboModel(parent,request,defaut)
        #init dates
        now=QtCore.QDate.currentDate()
        self.parent.dateEdit_consult.setDate(now)
        
        #connect actions
        #____________________________***   Tab_Consultation   ***__________________________
        self.parent.comboBox_consultType.currentIndexChanged.connect(self.OnTypeConsultation)
        self.parent.toolButton_TypeConsultation.clicked.connect(self.OnEditTypeConsultation)
        self.parent.comboBox_PathologieDomaine.currentIndexChanged.connect(self.OnDomaine)
        self.parent.connect(self.parent.comboBox_Pathologie, QtCore.SIGNAL("highlighted(int)"),self.OnPathologie)
        self.parent.connect(self.parent.textBrowser_consultations, QtCore.SIGNAL("anchorClicked(QUrl)"),self.OnConsultationSelect)
        self.parent.toolButton_comment.clicked.connect(self.EditCommentaire)
        self.parent.connect(self.parent.comboBox_veterinaire,QtCore.SIGNAL("OnEnter"),self.OnConsultantEnter)
        self.parent.toolButton_Pathologie.clicked.connect(self.EditPathologie)
        self.parent.pushButton_valider.clicked.connect(self.SaveConsultation)
        self.parent.pushButton_Nouveau.clicked.connect(self.OnNewConsultation)
        
    def SetAnimal(self,idEspece,idAnimal):
        self.idEspece=idEspece
        self.idAnimal=idAnimal
        self.MyPathologie.SetEspece(self.idEspece)
        self.FillConsultation_Combo()
        self.GetConsultations()
                   
    def FillConsultation_Combo(self):
        self.parent.comboBox_veterinaire.setModel(MyComboModel(self.parent,'GetConsultants'))
        self.parent.comboBox_Referant.setModel(MyComboModel(self.parent,'GetReferants'))
        self.parent.comboBox_consultType.setModel(MyComboModel(self.parent,'GetTypesConsultation'))
        self.parent.comboBox_PathologieDomaine.setModel(MyComboModel(self.parent,'GetDomaines',u'Tous'))
                                
    def GetConsultations(self):
        MyDossier=Consultations(self.DBase,self.idAnimal)
        self.parent.textBrowser_consultations.setText(MyDossier.Get())
        self.parent.splitter.resize(1021,820)
        
    def OnConsultationSelect(self,link):
        self.FillConsultation_Combo()
        self.NewConsultation=False
        self.idConsultation=int(link.toString().toAscii()[2:])
        if link.toString().toAscii()[1]=='C':
            self.FillFormConsultation()
        if link.toString().toAscii()[1]=='N':
            self.OnNewConsultation()   
        if link.toString().toAscii()[1]=='B':
            print 'view biologie'
        if link.toString().toAscii()[1]=='I':
            print 'view Images'
        if link.toString().toAscii()[1]=='c':
            print 'view Chirurgies'
        if link.toString().toAscii()[1]=='O':
            print 'view Ordonnance'
        if link.toString().toAscii()[1]=='T':
            print 'view Plan thérapeutique'     
      
    def FillFormConsultation(self):
        self.MyConsult.Get(self.idConsultation)
        self.parent.dateEdit_consult.setDate(self.MyConsult.DateConsultation)
#        self.dateTimeEdit_analyse.setDate(self.MyConsult.DateConsultation)
        self.parent.comboBox_veterinaire.setCurrentIndex(self.parent.comboBox_veterinaire.findText(self.MyConsult.Consultant))
        index=self.parent.comboBox_consultType.findData(self.MyConsult.TypeConsultation_idTypeConsultation)
        if index>-1:
            self.parent.comboBox_consultType.setCurrentIndex(index)
        if len(self.MyConsult.Referant)>0:
            self.parent.comboBox_Referant.setCurrentIndex(self.parent.comboBox_Referant.findText(self.MyConsult.Referant))
        self.parent.textEdit_consultObs.setText(self.MyConsult.Examen)
        self.parent.textEdit_consultTrait.setText(self.MyConsult.Traitement)
        self.parent.toolButton_comment.setToolTip(self.MyConsult.Commentaires)  
        if not self.MyConsult.DomainePathologie is None:
            self.parent.comboBox_PathologieDomaine.setCurrentIndex(self.parent.comboBox_PathologieDomaine.findText(QtCore.QString(self.MyConsult.DomainePathologie)))
        #TODO: debug si pas de pathologie
        index=self.parent.comboBox_Pathologie.findText(self.MyConsult.ConsultationPathologiesString())
        if index==-1 and not self.MyConsult.ConsultationPathologiesString().isEmpty():
            self.parent.comboBox_Pathologie.setVisible(False)
            self.parent.label_Pathologie.setText(QtCore.QString(u'                                       Pathologies multiples  >>>'))
            self.parent.label_Pathologie.setMaximumWidth(341)
        else:
            self.parent.label_Pathologie.setMaximumWidth(81)
            self.parent.label_Pathologie.setText(QtCore.QString(u'Pathologie'))
            self.parent.comboBox_Pathologie.setVisible(True)
            if index==-1:
                self.parent.comboBox_Pathologie.setCurrentIndex(0)
            else:
                self.parent.comboBox_Pathologie.setCurrentIndex(index)
        self.parent.splitter.resize(1021,460)
        
    def OnTypeConsultation(self):
        if self.parent.comboBox_consultType.currentText()==QtCore.QString("Référée".decode('utf8')):
            self.parent.label_Referant.setVisible(True)
            self.parent.comboBox_Referant.setVisible(True)
        else:
            self.parent.label_Referant.setVisible(False)
            self.parent.comboBox_Referant.setVisible(False)
            
    def OnEditTypeConsultation(self):
        id=self.parent.comboBox_consultType.Getid()
        new=[0,'','',True,'']
        model=MyModel('TypeConsultation',id)
#        model=MyTable('TypeConsultation',id)
        if not model.SetNew(new):
            print ('Le vecteur d\'initialisation n\'est pas valide')    #TODO: SendError
            return
        data=[[u'Libélé',1,45,1],[u'Remarque',1,120,2]]
        form=MyForm('type de consultation',data,self)
        form.SetModel(model, [1,2])
        if form.exec_():
            print 'update combobox'
        
    def OnDomaine(self):
        self.parent.comboBox_Pathologie.setModel(self.MyConsult.GetComboList(self.parent,'SelectPathologies(%i,%i)'%(self.MyPathologie.idEspece, self.parent.comboBox_PathologieDomaine.Getid()),u'Néant'))
        
    def OnPathologie(self,link):
        if link>0:
            txt=self.MyPathologie.GetDefinitionPathologie(self.parent.comboBox_Pathologie.itemData(link).toInt()[0])
            QtGui.QToolTip.showText(QtGui.QCursor.pos(), QtCore.QString(txt), widget=self.parent.comboBox_Pathologie)
     
    def OnConsultantEnter(self):
        print'Ouvre formulaire veto'
        
    def UpdateConsultation_mdl(self):
        #attributes: idConsultation,Animal_idAnimal,DateConsultation,TypeConsultation_idTypeConsultation,Personne_idConsultant,Personne_idReferant,
        #Personne_idReferent,Examen,Traitement,Actif,Commentaires
        self.MyConsult.idConsultation=self.idConsultation
        self.MyConsult.DateConsultation=self.parent.dateEdit_consult.date()      
        self.MyConsult.Personne_idConsultant=self.parent.comboBox_veterinaire.GetData()
        self.MyConsult.Consultant=self.parent.comboBox_veterinaire.currentText()
        self.MyConsult.TypeConsultation_idTypeConsultation=self.parent.comboBox_consultType.GetData()
        self.MyConsult.TypeConsultation=self.parent.comboBox_consultType.currentText()
        if self.parent.comboBox_Referant.isVisible():
            self.MyConsult.Personne_idReferant=self.parent.comboBox_Referant.GetData()
            self.MyConsult.Referant=self.parent.comboBox_Referant.currentText()
        else:
            self.MyConsult.Personne_idReferant=None
        self.MyConsult.Examen=self.parent.textEdit_consultObs.toPlainText()
        self.MyConsult.Traitement=self.parent.textEdit_consultTrait.toPlainText()
        self.MyConsult.Animal_idAnimal=self.idAnimal
        if self.parent.comboBox_Pathologie.isVisible():
            idpathologie=self.parent.comboBox_Pathologie.GetData()
            if idpathologie>0:
                if not self.MyConsult.CheckDoublonPathologieRef(idpathologie):
                    tmp=Core_Critere.CriteresConsultation(idpathologie,self)
                    self.MyConsult.ConsultationPathologies.append(tmp)
            
    def SaveConsultation(self):
        self.UpdateConsultation_mdl()
        self.idConsultation=self.MyConsult.Save()
        #TODO: tooltip "Sauvegarde réussie"ou bouton disabled. Enabled apres saisie,onConsultation select, On NewConsulatation
        self.NewConsultation=True
             
    def EditCommentaire(self):
        form=FormComment()
        form.plainTextEdit.insertPlainText(self.MyConsult.Commentaires)
        if form.exec_():
            self.MyConsult.Commentaires=form.plainTextEdit.toPlainText()
            self.parent.toolButton_comment.setToolTip(QtCore.QString(self.MyConsult.Commentaires))
      
    def OnNewConsultation(self):
        self.NewConsultation=True
        self.idConsultation=0
        self.parent.dateEdit_consult.setDate(QtCore.QDate.currentDate())
        self.parent.comboBox_veterinaire.setCurrentIndex(0)
        self.parent.comboBox_consultType.setCurrentIndex(self.TypeConsultationDefaut)
        self.parent.comboBox_Referant.setCurrentIndex(0)
        self.parent.label_Pathologie.setMaximumWidth(81)
        self.parent.label_Pathologie.setText(QtCore.QString(u'Pathologie'))
        self.parent.comboBox_Pathologie.setVisible(True)
        self.parent.comboBox_PathologieDomaine.setCurrentIndex(0)
        self.parent.label_Referant.setVisible(False)
        self.parent.comboBox_Referant.setVisible(False)
        self.parent.textEdit_consultObs.clear()
        self.parent.textEdit_consultTrait.clear()
        self.parent.toolButton_comment.setToolTip(QtCore.QString('Ajouter un Commentaire'))
        self.parent.splitter.resize(1021,470) 
    
    def EditPathologie(self):
        #TODO: save Consultation & update idConsultation
        self.SaveConsultation()
        if self.editPathologie is None:
            self.editPathologie = FormPathologie(self)
        if self.editPathologie.exec_():
            self.editPathologie.tableWidget_Criteres.clearContents()
            self.editPathologie.NbCriteres=0
            print 'Pathologie éditée'
     
      
            
class FormComment(QtGui.QDialog):   #TODO: MyGeneric form
    def __init__(self,parent=None):
        super(FormComment,self).__init__(parent)
        self.resize(400, 255)
        self.setWindowTitle("Edition Consultation")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 17))
        self.label.setText("Entrez votre commentaire :")
        self.plainTextEdit = QtGui.QPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 361, 141))
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GuiConsultation()
    window.show()
    window.OnSelectAnimal()
    sys.exit(app.exec_())
