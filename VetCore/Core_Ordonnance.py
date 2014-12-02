# -*- coding: utf8 -*-
#import Tables
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import htql
import codecs

import config
from DBase import Request
from MyGenerics import *

class Ordonnance(MyModel):
    def __init__(self,idTable=0,parent=None, *args):
        MyModel.__init__(self,'Ordonnance',idTable,parent, *args)
        self.Animal=None        #contains animal properties :idAnimal,Nom,Race,idEspeces,Sexe,Age(years),identification,Poids
        self.Pathologies=[]     #contains Pathologies for the current consultation
        self.Lignes=[]
        
    def SetAnimal(self,idAnimal):
        self.Animal=self.MyRequest.GetLine('CALL GetAnimal(%i)'%idAnimal)
        
    def SetPathologies(self,idConsultation):
        self.Pathologies=self.MyRequest.GetLines('CALL GetPathologiesConsult(%i)'%idConsultation)
        
    def GetPoidsAnimal(self):
        if not self.Animal is None:
            return self.Animal[7].toString()


class Medicament(MyModel):
    def __init__(self, table,idTable,parent=None, *args):
        MyModel.__init__(self, table,idTable,parent=None, *args)
        self.idMedicament=idTable
        self.Presentation=None
        self.Posologie=None
        self.QuantDelivre=None
#         config.Path_ImportMed
#         config.Path_RCP

    def Reinit(self):
        self.listdata=self.MyRequest.GetLineTable(self.listdata[0].toInt()) 
           
    def Setid(self,idMedicament):
        self.idMedicament=idMedicament
    
    def GetCip(self):
        return self.listdata[3].toString()
    
    def SetRCP(self,filename):
        self.listdata[8]=QVariant(filename)
        
    def GetRCP(self):
            return self.listdata[8].toString()
        
    def GetPresentations(self,idMedicament):
        self.Presentation=None
        return self.MyRequest.GetLines('CALL GetPresentationMenu(%i)'%idMedicament)
        
    def Download(self,cip):
        if os.system('curl \"http://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid=%s&typedoc=R\" -o %srcptmp.html'%(cip,config.Path_ImportMed))>0:
            MyError(self.parent,u'RCP non trouvée en téléchargement')
            return
        else:
            #Clean imported html file
            myfile=open(config.Path_ImportMed+'rcptmp.html','r')
            html=''.join(myfile.readlines())
            myfile.close()
            sel=htql.HTQL(html,"<div(id=\'container\')>:tx")
            sel=htql.HTQL(sel[0],"<div(id=\'contentPrincipal\')>:tx")
            sel=htql.HTQL(sel[0],"<div(id=\'contentDocument\')>:tx")
            sel=htql.HTQL(sel[0],"<p(class=\'alignright\')>:&delete")
            sel=htql.HTQL(sel[0],"<a(href=\'#HautDePage\')>:&delete")
            sel=sel[0].replace('<p class=AmmDenomination>','<p class=AmmDenomination style=\'font-weight: bold; height: 20px\'>')
            sel=sel.replace('\x92','\'')        
            outfile=open(config.Path_ImportMed+'rcptmp.html','w')
            outfile.write(sel)
            outfile.close()
            
class FormRCP(QDialog): 
    def __init__(self,Medicament,RCP_txt,parent=None):
        QDialog.__init__(self,parent)
        self.parent=parent
        self.Medicament=Medicament
        self.setWindowTitle('Edition de la RCP')
        self.verticalLayout = QVBoxLayout(self)
        self.editor=QTextEdit(self)
        self.editor.setHtml(RCP_txt)
        self.verticalLayout.addWidget(self.editor)
        self.horizontalLayout = QHBoxLayout()
        self.pushButton_Cancel = QPushButton(self)
        self.pushButton_Cancel.setMinimumSize(QSize(0, 27))
        self.pushButton_Cancel.setText(u'Annuler')
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        self.pushButton_Add = QPushButton(self)
        self.pushButton_Add.setMinimumSize(QSize(0, 27))
        self.pushButton_Add.setText(u'Extraire')
        self.horizontalLayout.addWidget(self.pushButton_Add)
        self.pushButton_Delete = QPushButton(self)
        self.pushButton_Delete.setMinimumSize(QSize(0, 27))
        self.pushButton_Delete.setText(u'Supprimer')
        self.horizontalLayout.addWidget(self.pushButton_Delete)
        self.pushButton_Valid = QPushButton(self)
        self.pushButton_Valid.setMinimumSize(QSize(0, 27))
        self.pushButton_Valid.setText(u'Valider')
        self.horizontalLayout.addWidget(self.pushButton_Valid)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        self.resize(800,700)
        
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        self.pushButton_Delete.clicked.connect(self.OnDelete)
        self.pushButton_Valid.clicked.connect(self.OnValid)
#        self.pushButton_Add.clicked.connect(self.OnNew)
        
    def OnDelete(self):
        if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de vouloir effacer cet élément?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.Yes:
            os.remove(config.Path_RCP+self.Medicament.GetRCP())
            self.Medicament.SetRCP(QVariant())
            self.Medicament.Update()
            self.accept()
    
    def OnValid(self):
        if self.Medicament.GetRCP().isNull():
            name=self.Medicament.GetCip()+'.html'
            self.Medicament.SetRCP(name)
            self.Medicament.Update()
#         with codecs.open(config.Path_RCP+name, encoding="windows-1252", mode="w") as f:    #encode codec: "utf-8"
#             f.write(self.editor.toHtml())
        fout=open(config.Path_RCP+name,'wt')
        fout.write(self.editor.toHtml())    
        fout.close()
        self.accept()
    
    def OnCancel(self):
        self.close()
        
class FormMedicament(MyForm):
    def __init__(self,Medicament,data,parent):
        MyForm.__init__(self,u'Edition de Médicament',data,parent)
        self.parent=parent
        self.Medicament=Medicament
        self.CompositionModel=MyTableModel(self,5,'GetCompositionMedicament(%i)'%Medicament.idMedicament)
        self.fields[6].setMinimumWidth(340)
        self.fields[6].setModel(self.CompositionModel)  
        self.AddMenuAction(self.fields[6],'Editer',self.OnEditComposition)       
        self.PresentationModel=MyTableModel(self,3,'GetPresentation(%i)'%Medicament.idMedicament)
        self.fields[7].setMinimumWidth(340)
        self.fields[7].setModel(self.PresentationModel) 
        self.fields[6].ResizeHeight()
        self.fields[7].ResizeHeight()
        self.adjustSize()
        self.fields[6].autoResize(0)
        self.fields[7].autoResize(0)
        self.AddMenuAction(self.fields[7],'Editer',self.OnEditPresentation) 
                
    def OnEditComposition(self):
        try:
            idComposition=self.fields[6].Getid()
        except:
            idComposition=0
        new=[0,0,self.Medicament.idMedicament,'',None,None,'',None,None,1,'']
        self.CompositionModel=MyModel(u'MedicamentConcentration',idComposition,self.parent)
        if not self.CompositionModel.SetNew(new):
            return      
        data=[[u'Principe actif',4,None,None,'Editer le principe actif'],[u'Concentration',1,60],[u'Concentration',1,8],[u'Unite',4,None,None,u'Editer les unités de composition phamaceutique'],
               [u'Unité galénique',1,60],[u'Unité galénique',8],[u'Unite',4,None,None,u'Editer les unités galéniques']]
        form=FormComposition(data,self.parent)
        form.SetModel(self.CompositionModel,{0:1,1:3,2:4,3:5,4:6,5:7,6:8})
        if form.exec_():
            self.CompositionModel=MyTableModel(self,5,'GetCompositionMedicament(%i)'%self.Medicament.idMedicament)
            self.fields[6].setModel(self.CompositionModel)  
        
    def OnEditPresentation(self):
        try:
            idPresentation=self.fields[7].Getid()
        except:
            idPresentation=0
        new=[0,self.Medicament.idMedicament,'',None,None,1,'']
        self.PresentationModel=MyModel(u'Presentation',idPresentation,self.parent)
        if not self.PresentationModel.SetNew(new):
            return      
        data=[[u'Presentation',1,120],[u'Unite Galenique',4,None,None,u'Editer les unités galéniques'],[u'Nb d\'unités',8]]
        form=FormPresentation(data,self.parent)
        form.SetModel(self.PresentationModel,{0:2,1:3,2:4})
        if form.exec_():
            self.PresentationModel=MyTableModel(self,3,'GetPresentation(%i)'%self.Medicament.idMedicament)
            self.fields[7].setModel(self.PresentationModel)
            
             
class FormMolecule(MyForm):
    def __init__(self,idMolecule,idEspece,parent):
        new=[0,'','',None,'',1,0]
        self.MoleculeModel=MyModel(u'Molecule',idMolecule,parent)
        if not self.MoleculeModel.SetNew(new):
            return      
        data=[[u'Ppe actif court',1,110],[u'Ppe actif long',1,110],[u'Remarque',3,200,80],[u'Famille Thérapeutique',7,None,None,None,2],
              ['',9,None,180,None,2],[u'Posologies',7,None,None,None,2],[u'',6,None,150,None,2]]
        MyForm.__init__(self,u'Edition de molécule',data,parent)
        self.SetModel(self.MoleculeModel,{0:2,1:1,2:4})
        self.parent=parent
        self.posologiesModel=MyTableModel(self,6,'GetPosologies(%i,%i)'%(idMolecule,idEspece))
        self.fields[6].setMinimumWidth(400)
        self.fields[6].setModel(self.posologiesModel)
        self.fields[6].ResizeHeight()
        self.adjustSize()
        self.fields[6].autoResize(0)
        #TODO: qtree
           
           
class FormPresentation(MyForm):
    def __init__(self,data,parent):
        MyForm.__init__(self,u'Edition de Présentations de Médicament',data,parent)
        self.parent=parent
#         self.fields[0].setReadOnly(True)
        self.fields[1].setModel(MyComboModel(self,'GetUnites_fortype(\'Galen\')'))
        self.fields[1].setMaximumSize(QSize(200,27))
        self.EditButtons[0].clicked.connect(self.EditUnites)

    def EditUnites(self):
        idUnite=self.fields[1].Getid()
        new=[0,'',False,True,False,False,True,False,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Galénique',2]]
        form=MyForm('Unités',data,self)
        form.SetModel(UniteModel,{0:1,1:3})
        if form.exec_():
            self.fields[1].setModel(MyComboModel(self.parent,'GetUnites_fortype(\'Galen\')'))
            self.fields[1].Setid(idUnite)
        

class FormComposition(MyForm):  
    def __init__(self,data,parent):
        MyForm.__init__(self,u'Edition de la composition de Médicament',data,parent)
        self.parent=parent
        self.fields[0].setModel(MyComboModel(self,'GetMolecules(0,0,1)'))   #every active molecule 
        self.fields[0].setMaximumSize(QSize(300,27))
        self.fields[3].setModel(MyComboModel(self,'GetUnites_fortype(\'Compo\')'))
        self.EditButtons[1].clicked.connect(self.EditCompoUnites) 
        self.fields[6].setModel(MyComboModel(self,'GetUnites_fortype(\'Galen\')'))
        self.EditButtons[0].clicked.connect(self.OnEditMolecule)
        self.EditButtons[2].clicked.connect(self.EditGalenUnites) 
    
    def OnEditMolecule(self):
        try:
            idMolecule=self.fields[0].Getid()
        except:
            idMolecule=0    
        idEspece=self.parent.comboBox_especeCible.Getid()   
        form=FormMolecule(idMolecule,idEspece,self.parent)
        if form.exec_():
            self.MoleculeModel=MyComboModel(self,'GetCompositionMedicament(%i)'%self.Medicament.idMedicament)
            self.fields[0].setModel(self.MoleculeModel)  
            self.fields[0].setCurrentIndex(idMolecule)
        
    def EditCompoUnites(self):
        idUnite=self.fields[3].Getid()
        new=[0,'',False,False,True,False,True,False,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Composition',2]]
        form=MyForm('Unités',data,self)
        form.SetModel(UniteModel,{0:1,1:3})
        if form.exec_():
            self.fields[3].setModel(MyComboModel(self.parent,'GetUnites_fortype(\'Compo\')'))
            self.fields[3].Setid(idUnite)
            
    def EditGalenUnites(self):
        idUnite=self.fields[6].Getid()
        new=[0,'',False,True,False,False,True,False,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Galénique',2]]
        form=MyForm('Unités',data,self)
        form.SetModel(UniteModel,{0:1,1:3})
        if form.exec_():
            self.fields[6].setModel(MyComboModel(self.parent,'GetUnites_fortype(\'Galen\')'))
            self.fields[6].Setid(idUnite)
            
            