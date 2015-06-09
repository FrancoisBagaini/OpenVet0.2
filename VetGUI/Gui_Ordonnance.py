#!/usr/bin/env python
# -*- coding: utf8 -*-

#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PySide import QtCore, QtGui
#sys.path.append('../VetCore')

import sys
import time
#import config

import re
from MyGenerics import *
from Core_Ordonnance import *


class GuiOrdonnance():
	def __init__(self,parent=None):
		#TODO: pointeur=sablier
		self.Actif=True
		self.Pharmacope="H"	#TODO set to "V"
		self.parent=parent
		self.parent.radioButton_PharmacopeVet.setChecked(True)
		self.parent.radioButton_PharmacopeHum.setChecked(False)
		self.parent.checkBox_Actif.setChecked(True)
		self.MyOrdonnance=Ordonnance(0,self.parent)
		self.MyMedicament=None
		self.parent.textEdit_Ordonnance.setHtml('<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />')
		self.parent.comboBox_Molecule.SetCompleter()
		self.parent.comboBox_Molecule.setModel(MyComboModel(self.parent,'GetMolecules(0,1)'),True)
		self.parent.connect(self.parent.comboBox_Molecule,SIGNAL("OnEnter"),self.OnSelectMolecule)
		self.parent.connect(self.parent.comboBox_Molecule,SIGNAL("activated(int)"),self.OnSelectMolecule)
		self.parent.connect(self.parent.textEdit_Ordonnance, SIGNAL("OnEdit"),self.OnEditPrescription)
		self.parent.comboBox_Molecule.clearEditText()
		
		self.parent.comboBox_Medicament.SetCompleter()
		self.parent.comboBox_Medicament.setModel(MyComboModel(self.parent,'GetMedicaments(\"\",\"%s\",1)'%self.Pharmacope),True) 
		self.parent.comboBox_Medicament.clearEditText()
		self.parent.connect(self.parent.comboBox_Medicament,SIGNAL("activated(int)"),self.OnSelectMedicament)
		self.parent.connect(self.parent.comboBox_Medicament,SIGNAL("ContextMenuActivated"),self.OnSelectPresentation)
		self.parent.connect(self.parent.comboBox_Molecule,SIGNAL("ContextMenuActivated"),self.OnSelectPosologie)
		self.parent.connect(self.parent.radioButton_PharmacopeVet,SIGNAL("toggled(bool)"),self.OnPharmacopeV)
		self.parent.connect(self.parent.radioButton_PharmacopeHum,SIGNAL("toggled(bool)"),self.OnPharmacopeH)
#		self.parent.connect(self.parent.comboBox_Molecule,SIGNAL("editTextChanged(QString)"),self.OnMoleculeChanged)
		self.parent.connect(self.parent.checkBox_Actif,SIGNAL("stateChanged(int)"),self.OnActif)
		
		#self.parent.textBrowser_medicament.doubleClicked.connect(self.OnEditRCP)	#TODO: implement MousePressed in derived class of QTextBrowser or QTextEdit
		self.parent.toolButton_DownloadRCP.clicked.connect(self.OnDownloadRCP)
		self.parent.toolButton_EditRCP.clicked.connect(self.OnEditRCP)
		self.parent.toolButton_EditMedicament.clicked.connect(self.OnEditMedicament)
		self.parent.toolButton_EditMolecule.clicked.connect(self.OnEditMolecule)
		self.parent.pushButton_toOrdonnance.clicked.connect(self.OnAdd2Ordonnance)
		self.parent.pushButton_toOrdonnance.setDisabled(True)
#		self.parent.dateEdit_ordonance.dateChanged.connect(self.OnUpdateDate)
		self.parent.toolButton_CommentLine.clicked.connect(self.OnAddCommentLine)
		self.parent.pushButton_ValidOrdonnance.clicked.connect(self.OnValidOrdonnance)
		
		self.parent.comboBox_Molecule.setFocus()
		self.EditedLine=None
		self.MyMedicament=Medicament('Medicament',0,0,self.parent)
		self.MyMolecule=Molecule('Molecule',0,self.parent)
		
	def SetAnimal(self,idEspece,idAnimal):
		self.idEspece=idEspece
		self.MyOrdonnance.SetAnimal(idAnimal)
		self.parent.lineEdit_poids.setText(self.MyOrdonnance.GetPoidsAnimal())
		
	def SetConsultation(self,idConsultation):
		text=self.MyOrdonnance.SetConsulation(idConsultation)
		if not text is None:
			self.parent.textEdit_Ordonnance.setHtml(text)

# 	def OnUpdateDate(self):
# 		nline=self.MyOrdonnance.Html
# 		self.MyOrdonnance.Html=nline
# 		self.parent.textEdit_Ordonnance.setHtml(nline)
		
	def OnActif(self,state):
		if state:
			self.Actif=True
		else:
			self.Actif=False
		self.MajCombos()
		
	def OnPharmacopeV(self,toggle):
		if toggle:
			self.Pharmacope="V"
		else:
			self.Pharmacope="H"
		self.MajCombos()
		
	def OnPharmacopeH(self,toggle):
		if toggle:
			self.Pharmacope="H"
		else:
			self.Pharmacope="V"
		self.MajCombos()
			
	def MajCombos(self): #TODO MajCombos(routine_mol,routine_med)
		self.parent.comboBox_Molecule.model().Set('GetMolecules(0,%i)'%self.Actif)
		#need to reinitiate MycomboBox model to update the Qcompleter
		self.parent.comboBox_Molecule.setModel(self.parent.comboBox_Molecule.model(),True)
		self.parent.comboBox_Medicament.model().Set('GetMedicaments(\"\",\"%s\",%i)'%(self.Pharmacope,self.Actif))
		self.parent.comboBox_Medicament.setModel(self.parent.comboBox_Medicament.model(),True)
	
	def OnSelectMolecule(self,index=None):
		idTable=self.parent.comboBox_Molecule.Getid()
		principeActif=self.parent.comboBox_Molecule.currentText()
		if index is None:
			index=self.parent.comboBox_Molecule.findText(principeActif,Qt.MatchStartsWith)
		if not principeActif.isEmpty():
			self.parent.comboBox_Molecule.setCurrentIndex(index)
			self.parent.comboBox_Medicament.model().Set('GetMedicaments(\"%s\",\"%s\",%i)'%(principeActif,self.Pharmacope,self.Actif))
			self.parent.comboBox_Medicament.setModel(self.parent.comboBox_Medicament.model(),True)
			self.MyMolecule=Molecule('Molecule',idTable,self.parent)
			posologies=self.MyMolecule.GetPosologies(self.idEspece)
			self.parent.comboBox_Molecule.SetPopup(posologies)
			if len(posologies)>0:
				self.parent.comboBox_Molecule.SelectPopup(0)
		else:
			self.MajCombos()
			self.parent.comboBox_Molecule.clearEditText()
			self.parent.comboBox_Medicament.clearEditText()

	def OnSelectMedicament(self,index):
		idTable=self.parent.comboBox_Medicament.Getid()
		medicament=self.parent.comboBox_Medicament.currentText()
		if self.MyMolecule.idMolecule==0:
			self.MyMedicament=Medicament('Medicament',idTable,0,self.parent)
			(idMolecule,principeActif)=self.MyMedicament.GetMolecule()
			self.MyMolecule=Molecule('Molecule',idMolecule,self.parent)
			posologies=self.MyMolecule.GetPosologies(self.idEspece)
			self.parent.comboBox_Molecule.SetPopup(posologies)
			if len(posologies)>0:
				self.parent.comboBox_Molecule.SelectPopup(0)
			#TODO for debugging:self.parent.comboBox_Medicament.SetProperty(2)
			self.parent.comboBox_Medicament.model().Set('GetMedicaments(\"%s\",\"%s\",%i)'%(principeActif,self.Pharmacope,self.Actif))
			self.parent.comboBox_Medicament.setModel(self.parent.comboBox_Medicament.model(),True)
		else:
			self.MyMedicament=Medicament('Medicament',idTable,self.parent.comboBox_Molecule.Getid(),self.parent)
		try:
			self.MyMedicament.idPosologie=self.parent.comboBox_Molecule.SelectionContext[0]
		except:
			self.MyMedicament.idPosologie=0
		self.MyMedicament.idPresentation=0
		self.parent.pushButton_toOrdonnance.setEnabled(True)
		self.parent.comboBox_Medicament.SetPopup(self.MyMedicament.GetPresentations(medicament))
		if not self.parent.comboBox_Medicament.GetProperty(2).isNull():
			self.parent.textBrowser_medicament.setSource(QUrl(config.Path_RCP+self.parent.comboBox_Medicament.GetProperty(2).toString()))

	def OnSelectPosologie(self):
		self.MyMedicament.idPosologie=self.parent.comboBox_Molecule.SelectionContext[0]
			
	def OnSelectPresentation(self):
		self.MyMedicament.Setid(self.parent.comboBox_Medicament.SelectionContext[0])		#idMedicament
		self.MyMedicament.idPresentation=self.parent.comboBox_Medicament.SelectionContext[1]
		
	def OnAdd2Ordonnance(self):
 		if self.MyMedicament.idPresentation==0:
 			MyError(self.parent,u'Vous devez renseigner la présentation avant d\'ajouter le médicament à l\'ordonnance')
 		else:
			poids=self.parent.lineEdit_poids.text().toFloat()
			if poids[1]:
				MyLignes=MyModel('LigneOrdonnance',0)
				MyLignes.SetNew([0,self.MyOrdonnance.idTable,None,None,None,None,None,None,None,None,u'',None,None,True,False,''])
				MyLignes.New()
				self.MyMedicament.GetLigneOrdonnance(poids[0],MyLignes)
				if not MyLignes is None:
					self.MyOrdonnance.Lignes.append(MyLignes)
					self.MyOrdonnance.WritePrescription()	
			else:
				MyError(self.parent,u'Poids non valide')

	def OnEditPrescription(self):
		(idline,line)=self.MyOrdonnance.GetLine(self.parent.textEdit_Ordonnance.Selection)
		if idline is None:
			self.parent.setStatusTip(u'Selection non trouvée')
			return
		self.EditedLine=line
		if line.listdata[2].isNull():
			self.parent.lineEdit_Remarque.setPlainText(line.listdata[10].toString())
		else:
			(self.MyMedicament.idMedicament,self.MyMedicament.idPresentation,self.MyMedicament.idMolecule,self.MyMedicament.idPosologie)=[i.toInt()[0] for i in line.listdata[2:6]]
			poids=self.parent.lineEdit_poids.text().toFloat()
			if poids[1]:
				self.MyMedicament.GetLigneOrdonnance(poids[0],line)
				if not line is None:
					if line.listdata[10].toString().isEmpty():
						del self.MyOrdonnance.Lignes[idline]
					else:
						self.MyOrdonnance.Lignes[idline]=line
					self.MyOrdonnance.WritePrescription()	
				
	def OnAddCommentLine(self):
		ligne=self.parent.lineEdit_Remarque.toPlainText()
		if not ligne.isEmpty():
			if not self.EditedLine is None:
				self.EditedLine.listdata[10]=QVariant(unicode(ligne))
			else:
				MyLignes=MyModel('LigneOrdonnance',0)
				MyLignes.SetNew([0,self.MyOrdonnance.idTable,None,None,None,None,None,None,None,None,unicode(ligne),None,None,True,False,''])
				MyLignes.New()
				self.MyOrdonnance.Lignes.append(MyLignes)
		else:
			if not self.EditedLine is None:
				del self.MyOrdonnance.Lignes[self.MyOrdonnance.Lignes.index(self.EditedLine)]	
		self.MyOrdonnance.WritePrescription()
		self.EditedLine=None
		self.parent.lineEdit_Remarque.clear()
							
	def OnDownloadRCP(self):
		if self.MyMedicament is None:
			return
		cip=str(self.parent.comboBox_Medicament.GetProperty(1).toString())[1:]
		if self.MyMedicament.Download(cip):
			self.parent.textBrowser_medicament.clear()
			self.parent.textBrowser_medicament.setSource(QUrl(config.Path_ImportMed+'rcptmp.html'))
		else:
			MyError(self.parent,u'RCP non trouvée en téléchargement')
	
	def OnEditRCP(self):
		if self.MyMedicament is None:
			return
		Myform=FormRCP(self.MyMedicament,self.parent.textBrowser_medicament.toHtml(),self.parent)
		if Myform.exec_():
			print u'RCP sauvegardée'
			
	def OnEditMedicament(self):
		idMedicament=self.MyMedicament.idMedicament
		new=[0,'','','',False,False,False,'',None,0.0,True,'']
		self.MedicamentModel=MyModel('Medicament',idMedicament,self.parent)
		if not self.MedicamentModel.SetNew(new):
			return	  
		data=[[u'Designation courte',1,60],[u'Designation longue',1,150],[u'Homéopathie',2],[u'Injectable',2],[u'Vaccin',2],
			[u'Galénique',1,120],[u'Composition',6],[u'Présentations',6]]
		form=FormMedicament(self.MyMedicament,data,self.parent)
		form.SetModel(self.MedicamentModel,{0:1,1:2,2:4,3:5,4:6,5:7})
		form.exec_()
		
	def OnEditMolecule(self):
		try:
			idMolecule=self.parent.comboBox_Molecule.Getid()
		except:
			idMolecule=0
		idEspece=self.MyOrdonnance.Animal[3].toInt()[0]
		form=FormMolecule(idMolecule,idEspece,self.parent)
		if form.exec_():
			self.parent.comboBox_Molecule.setModel(MyComboModel(self.parent,'GetMolecules(0,1)'),True)
			self.parent.comboBox_Molecule.setCurrentIndex(idMolecule)	
			
	def OnValidOrdonnance(self):
		self.MyOrdonnance.Save()
		if self.MyOrdonnance.lasterror is None:
			QToolTip.showText(QCursor.pos(),u'Sauvegarde réussie.')
