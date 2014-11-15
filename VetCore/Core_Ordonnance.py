# -*- coding: utf8 -*-
#import Tables
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import config
from DBase import Request
from MyGenerics import *

class Ordonnance(MyModel):
    def __init__(self,idTable=0,parent=None, *args):
        MyModel.__init__(self,'Ordonnance',idTable,parent, *args)
        self.Animal=None        #contains animal properties :idAnimal,Nom,Race,idEspeces,Sexe,Age(years),identification,Poids
        self.Pathologies=[]     #contains Pathologies for the current consultation
        
    def SetAnimal(self,idAnimal):
        self.Animal=self.MyRequest.GetLine('CALL GetAnimal(%i)'%idAnimal)
        
    def SetPathologies(self,idConsultation):
        self.Pathologies=self.MyRequest.GetLines('CALL GetPathologiesConsult(%i)'%idConsultation)
        
    def GetPoidsAnimal(self):
        if not self.Animal is None:
            return self.Animal[7].toString()

class Medicament:
    def __init__(self,parent):
        self.parent=parent
        self.Pharmacop="H"
#         config.Path_ImportMed
#         config.Path_RCP
        
    
    def Download(self,cip):
        if os.system('curl \"http://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid=%s&typedoc=R\" -o %srcptmp.html'%(cip,config.Path_ImportMed))>0:
            MyError(self.parent,'RCP non trouvée en téléchargement')
            return
        else:
            pass #display rcptmp.html