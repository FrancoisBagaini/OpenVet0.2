#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtCore, QtGui
#from PySide import QtCore, QtGui

from ui_Form_medical import Ui_tabWidget_medical
from Gui_Consultation import GuiConsultation
from Gui_Vaccination import GuiVaccination
from Gui_Analyse import GuiAnalyse
from Gui_Ordonnance import GuiOrdonnance


class TabMedical(QtGui.QTabWidget,Ui_tabWidget_medical):
    
    def __init__(self,db,parent=None):
        QtGui.QTabWidget.__init__(self,parent)
        self.setupUi(self)
        self.Qbase=db
        self.editClient = None
        self.editAnimal = None
        self.GuiConsultation=GuiConsultation(self)
        self.GuiVaccination=GuiVaccination(self)
        self.GuiAnalyse=GuiAnalyse(self)
        self.GuiOrdonnance=GuiOrdonnance(self)
        
    def SelectAnimal(self,idEspece,idAnimal):
        self.setVisible(True)
        self.GuiConsultation.SetAnimal(idEspece,idAnimal)
        self.GuiVaccination.SetAnimal(idEspece,idAnimal)
        self.GuiAnalyse.SetAnimal(idEspece,idAnimal)
        self.GuiOrdonnance.SetAnimal(idEspece,idAnimal)
        self.comboBox_consultType.hidePopup()
        self.comboBox_veterinaire.hidePopup()
        self.comboBox_Referant.hidePopup()
             
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TabMedical(None)
    window.show()
    sys.exit(app.exec_())
