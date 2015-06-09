# -*- coding: utf8 -*-
#import Tables
import time
from PyQt4 import QtCore
from PyQt4.QtGui import *
from Core_Pathologie import *
from Core_Critere import *

from DBase import Request
from MyGenerics import *

DATE,idCONSULTANT,idTYPECONSULTATION,idREFERANT,EXAMEN,TRAITEMENT,COMMENTAIRE,isACTIF,isDELETED,TYPECONSULTATION,CONSULTANT,REFERANT,isBIOLOGIE,isIMAGE,isCHIRURGIE,isORDONNANCE,isPLANTHERAPEUTIQUE = range(2,19)

class Consultation(MyModel):
	def __init__(self,idAnimal,idTable=0,parent=None, *args):
		#idConsultation,Animal_idAnimal,DateConsultation,idTypeConsultation,Personne_idConsultant,Personne_idReferant,Examen,Traitement,Commentaire,isActif,isDeleted
		self.idAnimal=idAnimal
		MyModel.__init__(self,'Consultation',idTable,parent, *args)
		self.SetConsultation(idTable)
		self.idConsultation=idTable
			
	def SetConsultation(self,idConsultation=0):
		self.idConsultation=idConsultation
		isexist=0
		if idConsultation>0:
			self.listdata=self.MyRequest.GetLineTable(idConsultation)
			listcomp=self.MyRequest.GetLineModel('CALL GetConsultation_comp(%i)'%idConsultation)
			self.listdata.extend(listcomp)
		else:
			self.SetNew(self.MyRequest.GetLineModel('CALL GetNewConsultation(%i)'%self.idAnimal))
			if not self.Newfields[0]==QVariant(0):
				isexist=self.Newfields[0]
				self.Newfields[0]=QVariant(0)
			self.New()
		self.GetPathologies()
		return isexist
			
	def MakeHTML(self):
		if self.idConsultation==0:
			return
		#idConsultation,Animal_idAnimal,DateConsultation,Personne_idConsultant,Personne_idReferant,Personne_idReferent,Examen,Traitement,Commentaire,isActif,isDeleted
		if self.Fdata(REFERANT).isEmpty():
			text="<a HREF=\"#C%i\"><b>%s</b></a>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp;<br>"%(self.idConsultation,self.Fdata(DATE),self.Fdata(CONSULTANT),self.Fdata(TYPECONSULTATION))
		else:
			text="<a HREF=\"#C%i\"><b>%s</b></a>&emsp;Dr %s&emsp;&emsp;Consultation %s&emsp; de %s<br>"%(self.idConsultation,self.Fdata(DATE),self.Fdata(CONSULTANT),self.Fdata(TYPECONSULTATION),self.Fdata(REFERANT))
		if self.Fdata(isBIOLOGIE):
			icone=':/newPrefix/images/analyse.png'
			tips=self.GetBiologies()
			text=text+"<a HREF=\"#B%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Biologie\" src=\"file:%s\"></a>"%(self.idConsultation,tips,icone)
		if self.Fdata(isIMAGE):
			icone='../images/echo.png'
			tips=self.GetImages()
			text=text+"<a HREF=\"#I%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Imagerie\" src=\"file:%s\"></a>"%(self.idConsultation,tips,icone)
		if self.Fdata(isCHIRURGIE):
			icone='../images/scalpel.png'
			tips=self.GetChirurgies()
			text=text+"<a HREF=\"#c%i\"><img title=\"%s\" style=\"width: 32px; height: 32px;\" alt=\"Chirurgie\" src=\"file:%s\"></a>"%(self.idConsultation,tips,icone)
		if self.Fdata(isORDONNANCE):
			icone='../images/doc_all.png'
			text=text+"<a HREF=\"#O%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Ordonnance\" src=\"file:%s\"></a>"%(self.idConsultation,icone)
		if self.Fdata(isPLANTHERAPEUTIQUE):
			icone='../images/planT.png'
			text=text+u"<a HREF=\"#T%i\"><img style=\"width: 32px; height: 32px;\" alt=\"Plan Thérapeutique\" src=\"file:%s\"></a>"%(self.idConsultation,icone)
		text=text+"&emsp;&emsp;&emsp;&emsp;<font color=\"red\">%s</font>"%self.LinePathologies
		text=text+"<br>%s<br><span style=\"text-decoration:underline;\">Traitements</span> : %s<br>"%(self.Fdata(EXAMEN),self.Fdata(TRAITEMENT))
		return text
	
	def GetBiologies(self):
		return self.MyRequest.GetString('CALL GetBiologies_line(%i)'%self.idConsultation, 0)
			
	def GetImages(self):
		return self.MyRequest.GetString('CALL GetImages_line(%i)'%self.idConsultation, 0)
		
	def GetChirurgies(self):
		return self.MyRequest.GetString('CALL GetChirurgie_line(%i)'%self.idConsultation, 0)
	
	def GetPathologies(self):
		self.Pathologies=Pathologies(self.idAnimal,self.idConsultation,self.ParentWidget)
		self.LinePathologies=self.Pathologies.LinePathologies
	
	def GetDomaine(self):
		return self.MyRequest.GetString('CALL IsDomaineUQ(%i)'%self.idConsultation, 0)
	
	def GetComment(self):
		return self.listdata[COMMENTAIRE].toString()
	
	def SetComment(self,text):
		self.listdata[COMMENTAIRE]=QVariant(text)
		
	def Save(self,isRefere,index):	#TODO:remove index?
		if isRefere.isNull():
			self.listdata[idREFERANT]=QVariant()
		if self.listdata[COMMENTAIRE].toString().simplified ().isEmpty():
			self.listdata[COMMENTAIRE]=QVariant()
		if self.listdata[EXAMEN].toString().simplified ().isEmpty() and self.listdata[TRAITEMENT].toString().simplified ().isEmpty():
			MyError(self.ParentWidget,u'Les champs Examen et Traitement ne peuvent pas être tous les deux Nuls.')
			return False
		#TODO: if Date>Now() MyConfirmation
		#TODO: begin transaction
		self.Update(index)
		if self.listdata[0]==0:
			self.listdata[0]=self.lastid
			self.idConsultation=self.listdata[0]
		self.Pathologies.Save(self.listdata[0])
		return True 

	
class Consultations:
	def __init__(self,parentwidget,idAnimal):
		self.consultations=[]
		self.textHTML=''
		self.ParentWidget=parentwidget
		self.idAnimal=idAnimal
		
	def Get(self):
		self.textHTML=''
		self.consultations=Request().GetInts("CALL GetConsultations_id(%i)"%self.idAnimal,0)
		for i in self.consultations:
			MyConsult=Consultation(self.idAnimal,i,self.ParentWidget)
			self.textHTML=self.textHTML+MyConsult.MakeHTML()+'<br>'
			del MyConsult
		icone='../images/add.png'
		self.textHTML=self.textHTML+"<a HREF=\"#N-1\"><img title=\"Nouvelle Consultation\" style=\"width: 32px; height: 32px;\" alt=\"Nouvelle Consultation\" src=\"file:%s\"></a>"%(icone)
		return self.textHTML


class FormTypeConsultation(MyForm):
	def __init__(self,idTable,data,parent):
		self.idTable=idTable
		MyForm.__init__(self,u'Type de Consultation',data,parent)
		new=[0,'','',0,0,1,0,'']
		model=MyModel('TypeConsultation',idTable,parent)
		if not model.SetNew(new):
			return
		self.SetModel(model, {0:1,1:2,2:3,3:4})
		
	def OnValid(self):
		if self.mapper.submit():
			self.MyModel.Update(self.mapper.currentIndex())
			if self.fields[2].isChecked():
				Request().Execute('UPDATE TypeConsultation SET isDefaut=FALSE WHERE NOT idTypeConsultation=%i'%self.idTable)
			self.accept()
		else:
			if self.mapper.model().lastError().type()==2:
				QMessageBox.warning(self,u"Alerte OpenVet",u'Cette entrée constitue un doublon', QMessageBox.Ok | QMessageBox.Default)

if __name__ == '__main__':
	import Tables
	import config 
	DBase=Tables.DataBase(config.database)
 	MyConsult=Consultation(DBase,1)
 	MyConsult.Get(1)
 	MyConsult.Print()
# 	print MyConsult.MakeHTML()
# 	MyConsults=Consultations(DBase,1)
# 	MyConsults.Get()
#	MyConsult.Print()
#	MyConsult.GetPathologiesConsultation()
#	MyConsult.GetConsultants()




