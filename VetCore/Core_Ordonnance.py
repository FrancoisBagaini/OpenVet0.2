# -*- coding: utf8 -*-
#import Tables
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import htql
import codecs
import re

import config
from DBase import Request
from MyGenerics import *
from Gui_Prescrire import *

class Ordonnance(MyModel):
    def __init__(self,idTable=0,parent=None, *args):
        MyModel.__init__(self,'Ordonnance',idTable,parent, *args)
        self.parent=parent
        self.idTable=idTable
        self.Date=None
        self.Prescripteur=None
        self.Consultation=None  #contains id,Date,4:idPrescripteur,5:Prescripteur,9:Pathologies,15:Nb Ordonnances (only one by consultation)
        self.Animal=None        #contains animal properties :idAnimal,Nom,Race,idEspeces,Sexe,Age(years),identification,Poids,idPoids
        self.Pathologies=[]     #contains Pathologies for the current consultation
        self.Lignes=[]
        self.Html='<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /></head><body></body></html>'
        
    def SetAnimal(self,idAnimal):
        self.Animal=self.MyRequest.GetLine('CALL GetAnimal(%i)'%idAnimal)
    
    def SetConsulation(self,idConsulation):   
        self.Consultation=self.MyRequest.GetLine('CALL GetConsultation(%i)'%idConsulation)
        self.Date=self.Consultation[1].toDate().toString('dd.MM.yyyy')
        Nord=self.MyRequest.GetString('SELECT NoOrdre FROM Personne WHERE idPersonne=%i'%self.Consultation[4].toInt()[0])
        Nord='123000'#debug only
        self.Prescripteur=self.Consultation[5].toString()+' (%s)'%Nord
        #TODO: GetPathologies
        
    def SetPathologies(self,idConsultation):
        self.Pathologies=self.MyRequest.GetLines('CALL GetPathologiesConsult(%i)'%idConsultation)
        
    def GetPoidsAnimal(self):
        if not self.Animal is None:
            return self.Animal[7].toString()

    def WritePrescription(self,nline):
        icone=config.Path_Icons+'edit1.png'
#        anchor="<a HREF=\"#P%i\"><img title=\"Editer la préscription\" style=\"width: 32px; height: 32px;\" alt=\"Editer la préscription\" src=\"file:%s\"></a>"%(len(self.Lignes),icone)
        nline='<b>'+nline[:nline.index('\n')]+'   </b><br>'+nline[nline.index('\n')+1:]+'<br>'
        nline=self.parent.textEdit_Ordonnance.toHtml().replace('<meta name=\"qrichtext\" content=\"1\" />','<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />')+unicode(nline)
        self.parent.textEdit_Ordonnance.setHtml(nline)   
 
    def GetLine(self,Selection):
        text=Selection.selectedText()
        for j,i in enumerate(self.Lignes):
            if str(text) in i[8]:
                return (j,i)
    
    def Save(self):
        pathologies=''
        html=self.parent.textEdit_Ordonnance.toHtml().replace('\"','\\"')
        new=[self.idTable,self.Consultation[0].toInt()[0],self.Consultation[4].toInt()[0],self.Animal[8].toInt()[0],pathologies,
             html,self.parent.lineEdit_Remarque.text(),True,False,'']
        self.SetNew(new)
        self.New()
        self.Update()
        #TODO valid Lignes & save Lignes

class Molecule(MyModel):
    def __init__(self, table,idTable,parent):
        MyModel.__init__(self, table,idTable,parent)
        self.idMolecule=idTable
        
    def GetPosologies(self,idEspece):
        self.Posologie=0
        return self.MyRequest.GetLines('CALL GetPosologieMenu(%i,%i)'%(self.idMolecule,idEspece))

class Medicament(MyModel):
    def __init__(self, table,idTable,idMolecule,parent=None, *args):
        MyModel.__init__(self, table,idTable,parent=None, *args)
        self.parent=parent
        self.table=table
        self.idMedicament=idTable
        self.idMolecule=idMolecule
        self.idPresentation=0
        self.idPosologie=0
#         config.Path_ImportMed
#         config.Path_RCP

#     def Reinit(self):
#         self.listdata=self.MyRequest.GetLineTable(self.listdata[0].toInt()) 
           
    def Setid(self,idMedicament):
        self.idMedicament=idMedicament
        self.listdata=self.MyRequest.GetLineTable(idMedicament)
    
    def GetCip(self):
        return self.listdata[3].toString()
    
    def SetRCP(self,filename):
        self.listdata[8]=QVariant(filename)
        
    def GetRCP(self):
            return self.listdata[8].toString()
        
    def GetPresentations(self,Medicament):
        self.idPresentation=0
        return self.MyRequest.GetLines('CALL GetPresentationMenu(\"%s\")'%Medicament)
    
    def GetEverything(self):
        return self.MyRequest.GetLine('CALL GetMyMedicament(%i,%i,%i,%i)'%(self.idMedicament,self.idPresentation,self.idMolecule,self.idPosologie))
    
    def GetMultiple(self,unite):
        convert={'':1,'m':1E-3,'µ':1E-6,'n':1E-9,'p':1E-12,'M':1E6}
        try:
            m=re.findall(r'g|l|UI|Eq|mol',unite)[0]
            return convert[unite[:unite.index(m)]]
        except:
            MyError(self.parent,u'Unité non reconnue <> g,l,UI,Eq,mol')
            return -1
            
    def CheckUniteFits(self,conc,poso):
        try:
            poso_qte=poso[:poso.index('/')]
            poso_patient=poso[poso.index('/')+1:]
        except:
            MyError(self.parent,u'Unité de posologie incorrecte')
            return -1
        if poso_qte==conc:
            return 1
        else:
            return self.GetMultiple(poso_qte)/self.GetMultiple(conc)
    
    def GetLigneOrdonnance(self,poids,values=None):
            m=self.GetEverything()
            dosemin=None
            maxadmin=None
            duree=''
            dose='?'
            if m[4].toFloat()[1] and m[4].toFloat()[1] and m[13].toFloat()[1] and m[14].toFloat()[1]:
                if m[4].toFloat()[0]==0:
                    MyError(self.parent,u'La composition du médicament n\'est pas valide')
                else:
                    rapport=self.CheckUniteFits(str(m[5].toString()),str(m[15].toString()))
                    if rapport!=-1:
                        dosemin=m[13].toFloat()[0]*poids*rapport/m[4].toFloat()[0]
                        dosemax=m[14].toFloat()[0]*poids*rapport/m[4].toFloat()[0]
                        if m[8].toString()==m[10].toString():
                            maxadmin=round(m[11].toInt()[0]*m[4].toFloat()[0]/(dosemin*rapport),1)
                            minadmin=round(m[11].toInt()[0]*m[4].toFloat()[0]/(dosemax*rapport),1)
                            dosemin=round(dosemin,3)
                            dosemax=round(dosemax,3)
                            dose='%.3f-%.3f %s(s)'%(dosemin,dosemax,m[8].toString())
                            duree='%.1f-%.1f admin'%(minadmin,maxadmin)
            else:
                MyError(self.parent,u'Posologie et/ou composition inconnue')
            info=u'Composition: %s pour %s.\nPrésentation: %s.'%(m[3].toString(),m[6].toString(),m[9].toString())
            data=[dose,duree,m[10].toString(),info,m[16].toString(),m[17].toString(),m[2].toString(),m[12].toString(),poids]
            MyForm=FormPrescrire(data,self.parent)
            if not values is None:
                MyForm.FillValues(MyForm,values[4:])
            if MyForm.exec_()==MyForm.Accepted:
                self.nline=str(MyForm.prescription) 
                idUniteGalenique=self.MyRequest.GetInt('SELECT Unite_idUnite FROM Presentation WHERE idPresentation=%i'%self.idPresentation)
                return (self.idMedicament,self.idPresentation,self.idMolecule,self.idPosologie,MyForm.dose,idUniteGalenique,MyForm.duree,MyForm.idtemps,str(MyForm.prescription),MyForm.delivre,MyForm.remarque)               

                    
    def Download(self,cip):
        if os.system('curl \"http://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid=%s&typedoc=R\" -o %srcptmp.html'%(cip,config.Path_ImportMed))>0:
            return False
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
            return True
            
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
        text=str(self.editor.toHtml())
        text=text.replace('<meta name=\"qrichtext\" content=\"1\" />','<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />')
        fout.write(text)    
        fout.close()
        self.accept()
 
# import htmlentitydefs,re,string
#  
# def stringhtml(chaine):
#     emap={}
#     for i in range(256):
#         emap[chr(i)]= "&%d;" % i
#  
#     for entity, char in htmlentitydefs.entitydefs.items():
#         if emap.has_key(char):
#             emap[char]="&%s;" % entity
#  
#     def remplace(m,get=emap.get):
#         return string.join(map(get,m.group()),"")
#  
#     return re.sub(r'[&<>\"\x80-\xff]+', remplace, chaine)
#  
# chaine='à == ç == è == ù == û == è == & == ë "'
# print chaine
# print stringhtml(chaine)

        # convertir texte en unicode
        #texte = "é".decode('utf-8')
        # variante : texte = u"é"
        # convertir unicode non-ascii en HTML
        #texte.encode('ascii', "xmlcharrefreplace")
    
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
        self.idMolecule=idMolecule
        new=[0,'','',None,'',1,0]
        self.MoleculeModel=MyModel(u'Molecule',idMolecule,parent)
        if not self.MoleculeModel.SetNew(new):
            return      
        data=[[u'Ppe actif court',1,110],[u'Ppe actif long',1,110],[u'Remarque',3,200,80],[u'Famille Thérapeutique',7,None,None,None,2],
              ['',9,None,180,None,2],[u'Posologies',7,None,None,None,2],[u'',6,None,150,None,2]]
        MyForm.__init__(self,u'Edition de molécule',data,parent)
        self.InactivateEnter()
        self.parent=parent
        #Fill Posologies
        self.posologiesModel=MyTableModel(self,6,'GetPosologies(%i,%i)'%(idMolecule,idEspece))
        self.fields[6].setMinimumWidth(400)
        self.fields[6].horizontalHeader().setResizeMode(QHeaderView.Interactive)
        self.fields[6].setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum)
        self.fields[6].setModel(self.posologiesModel)
        self.fields[6].ResizeHeight()
        self.adjustSize()
        self.fields[6].ResizeHeight()
        self.fields[6].autoResize(0)
        action=self.popMenus[1].addAction('Editer')
        self.connect(action,SIGNAL("triggered()"),self.OnEditPosologie)
        #Fill Classes Thérapeutiques and select
        self.CurrentClassTher=None
        self.classesTherModel=MyTreeModel(self,u'Classes Thérapeutiques','GetClassesTherapeutiques()')
        self.fields[4].setModel(self.classesTherModel)
        #        self.SetModel(self.MoleculeModel,{0:2,1:1,2:4})
        self.SetModel(self.MoleculeModel,{0:2,1:1,2:4,4:3})
        self.connect(self.fields[4],SIGNAL("activated(QModelIndex)"),self.OnSelectClassTher)
        
    def OnEditPosologie(self):
        idPoso=self.fields[6].Getid()
        idEspece=self.fields[6].model().data(self.fields[6].currentIndex(),34)
        idVoieAdmin=self.fields[6].model().data(self.fields[6].currentIndex(),35)
        self.PosologieModel=MyModel(u'MoleculePosologie',idPoso,self.parent)
        new=[0,self.idMolecule,idEspece,idVoieAdmin,None,0.0,0.0,32,'',None,1,0,'']
        if not self.PosologieModel.SetNew(new):
            return      
        data=[[u'Espèce',4,None,None,u'Editer les espèces'],[u'Voie d\'administration',4,None,None,u'Editer les voies d\'administration'],[u'Autre administration',1,80],[u'Posologie Min',1,10],[u'Posologie Max',1,10],
              [u'Unité',4,None,None,u'Editer les unités de posologie'],[u'Fréquence',1,80],[u'Remarque',3,200,80]]
        form=FormPosologie(data,self.parent)
        form.SetModel(self.PosologieModel,{0:2,1:3,2:4,3:5,4:6,5:7,6:8,7:9})
        if form.exec_():
            self.posologiesModel=MyTableModel(self,6,'GetPosologies(%i,%i)'%(self.idMolecule,idEspece))
            self.fields[6].setModel(self.posologiesModel)
    
    def OnSelectClassTher(self,index):
        self.classesTherModel.children[self.CurrentClassTher].setForeground(QBrush(QColor('darkgrey')))#TODO getdefault color
        self.CurrentClassTher=index.data(Qt.UserRole).toInt()[0] 
        self.classesTherModel.children[self.CurrentClassTher].setForeground(QBrush(QColor('red')))
        

class FormPosologie(MyForm):
    def __init__(self,data,parent):
        self.parent=parent
        MyForm.__init__(self,u'Edition de la Posologie',data,parent)
        self.fields[0].setModel(MyComboModel(self.parent,'GetEspeces()'))
        self.fields[1].setModel(MyComboModel(self.parent,'GetVoiesAdmin()'))
        self.fields[5].setModel(MyComboModel(self.parent,'GetUnites_fortype(\'Posol\')'))
        self.EditButtons[0].clicked.connect(self.OnEditEspece)
        self.EditButtons[1].clicked.connect(self.OnEditVoieAdmin)
        self.EditButtons[2].clicked.connect(self.OnEditUnite)
        
    def OnEditEspece(self):
        idEspece=self.fields[0].Getid()
        EspeceModel=MyModel(u'Especes',idEspece,self.parent)
        new=[0,'',None,1,0,'']
        if not EspeceModel.SetNew(new):
            return      
        data=[[u'Espèce',1,60],[u'Remarque',3,200,80]]
        form=MyForm(u'Edition des espèces',data,self.parent)
        form.SetModel(EspeceModel,{0:1,1:2})
        if form.exec_():
            self.fields[0].setModel(MyComboModel(self.parent,'GetEspeces()'))
            if not form.MyModel.lastid is None:
                self.fields[0].Setid(form.MyModel.lastid.toInt()[0])
            else:
                self.fields[0].Setid(idEspece)

    def OnEditVoieAdmin(self):
        idVoie=self.fields[1].Getid()
        VoieModel=MyModel(u'VoieAdministration',idVoie,self.parent)
        new=[0,'','',1]
        if not VoieModel.SetNew(new):
            return      
        data=[[u'Voie d\'administration',1,45],[u'Abréviation',1,12]]
        form=MyForm(u'Edition des voies d\'administration',data,self.parent)
        form.SetModel(VoieModel,{0:1,1:2})
        if form.exec_():
            self.fields[1].setModel(MyComboModel(self.parent,'GetVoiesAdmin()'))
            if not form.MyModel.lastid is None:
                self.fields[1].Setid(form.MyModel.lastid.toInt()[0])
            else:
                self.fields[1].Setid(idVoie)
                
    def OnEditUnite(self):
        idUnite=self.fields[5].Getid()
        new=[0,'',False,True,False,False,False,True,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Posologie',2]]
        form=MyForm(u'Unités de posologie',data,self)
        form.SetModel(UniteModel,{0:1,1:3})
        if form.exec_():
            self.fields[5].setModel(MyComboModel(self.parent,'GetUnites_fortype(\'Posol\')'))
            if not form.MyModel.lastid is None:
                self.fields[5].Setid(form.MyModel.lastid.toInt()[0])
            else:
                self.fields[5].Setid(idUnite)
        
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
        form=MyForm(u'Unités galénique',data,self)
        form.SetModel(UniteModel,{0:1,1:3})
        if form.exec_():
            self.fields[1].setModel(MyComboModel(self.parent,'GetUnites_fortype(\'Galen\')'))
            if not form.MyModel.lastid is None:
                self.fields[1].Setid(form.MyModel.lastid.toInt()[0])
            else:
                self.fields[1].Setid(idUnite)
        

class FormComposition(MyForm):  
    def __init__(self,data,parent):
        MyForm.__init__(self,u'Edition de la composition de Médicament',data,parent)
        self.parent=parent
        self.fields[0].setModel(MyComboModel(self,'GetMolecules(0,1)'))   #every active molecule 
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
            
            