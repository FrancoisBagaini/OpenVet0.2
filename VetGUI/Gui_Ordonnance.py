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

from MyGenerics import *
from Core_Ordonnance import *


class GuiOrdonnance():
	def __init__(self,parent=None):
		self.Actif=True
		self.Pharmacope="H"	#TODO set to "V"
		self.parent=parent
		self.parent.radioButton_PharmacopeVet.setChecked(True)
		self.parent.radioButton_PharmacopeHum.setChecked(False)
		self.parent.checkBox_Actif.setChecked(True)
		self.parent.dateEdit_ordonance.setDate(QDate.currentDate())
		self.MyOrdonnance=Ordonnance(0,self.parent)
		
		#TODO set combos medicament, molecule, presentation
		self.parent.comboBox_Molecule.setModel(MyComboModel(self.parent,'GetMolecules(0,0,1)'))
		self.parent.connect(self.parent.comboBox_Molecule,SIGNAL("OnEnter"),self.OnSelectMolecule)
		self.parent.comboBox_Molecule.clearEditText()
		self.parent.comboBox_Medicament.setModel(MyComboModel(self.parent,'GetMedicaments(\"\",\"%s\",1)'%self.Pharmacope)) 
		self.parent.comboBox_Medicament.clearEditText()
		
		self.parent.connect(self.parent.radioButton_PharmacopeVet,SIGNAL("toggled(bool)"),self.OnPharmacopeV)
		self.parent.connect(self.parent.radioButton_PharmacopeHum,SIGNAL("toggled(bool)"),self.OnPharmacopeH)
#		self.parent.connect(self.parent.comboBox_Molecule,SIGNAL("editTextChanged(QString)"),self.OnMoleculeChanged)
		self.parent.connect(self.parent.checkBox_Actif,SIGNAL("stateChanged(int)"),self.OnActif)
		
	def SetAnimal(self,idEspece,idAnimal):
		self.idEspece=idEspece
		self.parent.comboBox_especeCible.setModel(MyComboModel(self.parent,'GetEspeces()'))
		self.parent.comboBox_especeCible.Setid(idEspece)
		self.MyOrdonnance.SetAnimal(idAnimal)
		self.parent.lineEdit_poids.setText(self.MyOrdonnance.GetPoidsAnimal())

		#TODO : ordonnances existantes
		
	def SetConsultation(self,idConsultation):
		self.idConsultation=idConsultation
		#TODO : get pathologies	
#		self.MyConsultation= Consultation(self.idAnimal,0,self.parent)

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
			
	def MajCombos(self):
		self.parent.comboBox_Molecule.model().Set('GetMolecules(0,0,%i)'%self.Actif)
		self.parent.comboBox_Medicament.model().Set('GetMedicaments(\"\",\"%s\",%i)'%(self.Pharmacope,self.Actif))
	
	def OnSelectMolecule(self):
		principeActif=self.parent.comboBox_Molecule.currentText()
		index=self.parent.comboBox_Molecule.findText(principeActif,Qt.MatchStartsWith)
		if not principeActif.isEmpty():
			self.parent.comboBox_Molecule.setCurrentIndex(index)
			self.parent.comboBox_Medicament.model().Set('GetMedicaments(\"%s\",\"%s\",%i)'%(principeActif,self.Pharmacope,self.Actif))
		else:
			self.parent.comboBox_Medicament.model().Set('GetMedicaments(\"\",\"%s\",%i)'%(self.Pharmacope,self.Actif))
		self.parent.comboBox_Medicament.clearEditText()
			