#!/usr/bin/env python
# -*- coding: utf8 -*-
#******************************************************************************************************************
# Table: ResultatAnalyse
# fields:
# 0.idResultatAnalyse
#   Analyse_idAnalyse
#   Parametre_id    (NULL for doc)
#   ValeurQuant     (NULL for doc)
#   ValeurQual      (NULL for doc)
# 5.TitreDocument   (NULL for prm)
#   FichierExterne  (NULL for prm)
#   Etiquette       (NULL for prm)
# 8.Remarque        
# 9.isDeleted
# 
# Model ResultatAnalyseImage
# idResultatAnalyse
# Titre
# Etiquette
# FichierInterne
# Remarque
# isDirty
#********************************************************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import os
import sys
import hashlib
import config
from DBase import Request
from Viewer import DocViewer
from MyGenerics import *
import Mywidgets
from PyQt4.QtGui import *

class FormParametre(MyForm):
    def __init__(self,idparametre,data,parent):
        MyForm.__init__(self,u'Paramètre d\'analyse',data,parent)
        self.parent=parent
        self.InactivateEnter()
        self.idparametre=idparametre
        self.fields[2].setTristate(False)
        self.fields[3].setModel(MyComboModel(self.parent,'GetAllUnites()'))
        self.EditButtons[0].clicked.connect(self.OnEditUnite)
        self.connect(self.fields[2],SIGNAL("stateChanged(int)"),self.OnQuantitatif)
        
    def OnEditUnite(self):
        idUnite=self.fields[3].Getid()
        new=[0,'',False,True,False,'']
        UniteModel=MyModel('Unite',idUnite,self)
        if not UniteModel.SetNew(new):
            return  
        data=[[u'Unite',1,20],[u'Concentration',2]]
        form=MyForm('Unités',data,self)
        form.SetModel(UniteModel,{0:1,1:2})    #GUI_field : DB_Field
        if form.exec_():
            self.fields[3].setModel(MyComboModel(self.parent,'GetUnites()'))
            self.fields[3].Setid(idUnite)
            
    def OnQuantitatif(self,state):
        state=state!=0
        for i in range(3,6):
            self.fields[i].setVisible(state)
            self.labels[i].setVisible(state)
        self.EditButtons[0].setVisible(state)
            

class FormModeleAnalyse(MyForm):
    def __init__(self,data,parent):
        MyForm.__init__(self,u'Modèle d\'analyse',data,parent)
        self.parent=parent
        self.InactivateEnter()
#        self.fields[1].setModel(MyComboModel(self.parent,'GetAllUnites()'))


class ModelViewParameters(MyTableModel):
    def __init__(self, parent,nbHeaders,request,cols=None, *args): 
        MyTableModel.__init__(self, parent,nbHeaders,request,cols=None, *args)
         
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not index.row() < self.rowCount():
            return False
        value=QVariant(value)
        if role == Qt.EditRole:
            self.listdata[index.row()][index.column()+1]=value
            if self.data(index,34):
                if value.toFloat()<self.listdata[index.row()][4].toFloat() or value.toFloat()>self.listdata[index.row()][5].toFloat():
                    self.listdata[index.row()][self.NbCols+2]=QVariant(7)
                else:
                    self.listdata[index.row()][self.NbCols+2]=QVariant(0)
        elif role == Qt.UserRole:
            self.listdata[index.row()][0]=value
        elif role == Qt.ToolTipRole:
            self.listdata[index.row()][self.NbCols+1]=value
        elif role == Qt.ForegroundRole:
            self.listdata[index.row()][self.NbCols+2]=value
        elif role == 33:    #isDeleted
            self.listdata[index.row()][self.NbCols+3]=value
        elif role > 33:    #UserProperty
            self.listdata[index.row()][self.NbCols+3+role-33]=value
        else: 
            return False
        if role!=33:
            self.dirty = True
            self.SignId(index)
        else:
            self.SignId(index,False)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index,index)
        return True

    def InsertModelAnalyse(self,idModelAnalyse,idAnalyse):
        data=self.Myrequest.GetTableList(5,'CALL GetModelParametres(%i)'%idModelAnalyse)
        for i in data:
            i.extend([QVariant(idAnalyse),QVariant()])
            self.insertRows( self.rowCount(), i, rows=1, index=QModelIndex())
            
    def SetIdAnalyse(self,idAnalyse):
        for i in self.listdata:
            i[11]=QVariant(idAnalyse)
            
    def GetListParameters(self):
        Mylist=[]
        for i in self.listdata:    
            Mylist.append([i[0],i[1],"",QVariant(0),QVariant(0)])
        return Mylist
    
    def Update(self,table,maplist,parent,idindex=0,delindex=4):
        if not self.dirty:
                return
        for i in self.listdata:
            id=i[idindex].toInt()[0]
            if id<=0 and not i[delindex].toBool():
                if i[9].toBool():
                    i[3]=QVariant()       #Valeur Qualitative=NULL
                else:
                    i[2]=QVariant()      #Valeur Quantitative=NULL
                self.EditItem(i,table,maplist,idindex,delindex,parent)
            elif i[delindex].toBool() and id!=0:
                self.DeleteItem(table,abs(id),parent)


class Analyse(QSqlTableModel):
    def __init__(self, parent=None, *args):  # parentGui_Consultation
        QSqlTableModel.__init__(self, parent, *args)
        # attributes: idAnalyse,Consultation_idConsultation,TypeAnalyse_idTypeAnalyse,DateHeure,DescriptionAnalyse,Prelevement,SyntheseAnalyse,Conclusions
        self.parent=parent 
        self.idAnalyse = None
        self.idEspece = None
        self.idModeleAnalyse=None
        self.isImage = None
        self.setTable('Analyse')   
        self.select()
        self.mapper = QDataWidgetMapper(parent)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self)
        self.mapper.setItemDelegate(TypeAnalyseDeleguate(parent))
        self.mapper.addMapping(parent.dateTimeEdit_analyse, 3)
        self.mapper.addMapping(parent.lineEdit_description, 4)
        self.mapper.addMapping(parent.lineEdit_prelevement, 5)
        self.mapper.addMapping(parent.plainTextEdit_syntheseanalyse, 6)
        self.mapper.addMapping(parent.plainTextEdit_conclusions, 7)
        self.mapper.addMapping(parent.comboBox_typeanalyse, 2)
        self.Resultats = None
        self.Documents =None
    
    def IsImage(self):
        self.isImage=Request().GetInt("CALL IsAnalyseImage(%i)" % self.idAnalyse, 0)
        return self.isImage
    
    def Get(self, idAnalyse, idConsultation, idEspece):
        self.idAnalyse = idAnalyse
        self.idConsultation = idConsultation
        self.idEspece = idEspece
        if idAnalyse == 0:
            self.setFilter('idAnalyse>0')
            row = self.rowCount()
            self.insertRow(row)
            self.mapper.setCurrentIndex(row)    #Not a valid record for QSQLTable
            self.setData(self.index(row, 0), QVariant(0), Qt.EditRole)
            self.setData(self.index(row, 1), QVariant(self.idConsultation), Qt.EditRole)
            self.setData(self.index(row, 3), QVariant(QDateTime.currentDateTime()), Qt.EditRole)
            self.Documents = ResultatAnalyseImage(0)
        else:
            self.setFilter('idAnalyse=%i' % idAnalyse)
            self.mapper.toFirst()
            self.isImage =self.IsImage()
            self.Documents = ResultatAnalyseImage(idAnalyse)  
                        
    def Delete(self,idAnalyse):
        #TODO supprimer ResultatAnalyse Avant
        errAnalyse=Request('CALL DeleteItemTable(%i,"Analyse")'%idAnalyse)
        
    def Save(self):
        valid = QString(u'Analyses sauvegardées')
        self.mapper.submit()
        #TODO:BeginTransaction
        self.submitAll()
        errAnalyse = self.lastError()
        if not errAnalyse.isValid() or (errAnalyse.isValid() and errAnalyse.text().compare(' No Fields to update') == 0):
            if self.idAnalyse == 0:
                self.idAnalyse = Request().GetInt("SELECT LAST_INSERT_ID()", 0)
                self.parent.tableView_Parametres.model().SetIdAnalyse(self.idAnalyse)
            if not self.isImage:      
                self.parent.tableView_Parametres.model().Update('ResultatAnalyse',[0,11,10,2,2,12,12,12,6,8],self.parent,0,8)
                if not self.idModeleAnalyse is None:
                    MyRequest=Request('ModeleAnalyse')
                    MyRequest.Update(['idModeleAnalyse','LastSelection'],['%i'%self.idModeleAnalyse,'\"%s"'%QDate.currentDate().toString('yyyy-MM-dd')])
            else:
                errResultats = self.Documents.Save(self.idAnalyse)
                if errResultats.isValid():
                    valid = errResultats.text()
                    MyError(self.parent,errResultats.text())
            #TODO: maj lastselection modele
        else:
            valid = errAnalyse.text()
        return valid   
        
class ResultatAnalyseImage(QAbstractListModel): #=>MyCombomodel
    def __init__(self, idAnalyse, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args) 
        self.Myrequest = Request()
        self.MyViewer=DocViewer()
        self.listdata = self.Myrequest.GetLines('CALL GetResultatImage(%i)' % idAnalyse)
        self.maxiconesize=QSize(128,96)
        self.isChanged = False
        self.CurrentIndex = 0
        self.Deleted = []
                
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            if self.listdata[index.row()][1].toString().isEmpty():
                return QVariant(self.listdata[index.row()][2])
            else:
                return QVariant(self.listdata[index.row()][1])
        elif index.isValid() and role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif index.isValid() and role == Qt.ToolTipRole:
            return QVariant(self.listdata[index.row()][3])
        elif index.isValid() and role == Qt.DecorationRole:
            self.MyViewer.SetFilename('../Archives/%s'%self.listdata[index.row()][2].toString())
            return self.MyViewer.ViewImage(self.maxiconesize)
        else: 
            return QVariant()
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            self.listdata[index.row()][1] = value   
            self.listdata[index.row()][5] = QVariant(True)   
            self.isChanged = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return False
    
    def GetDocument(self,index):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            return [self.listdata[index.row()][1].toString(),self.listdata[index.row()][3].toString()]
            
    def GetRemarque(self, index):
        if index.isValid() and index.row() < self.rowCount():
            self.CurrentIndex = index
            return self.listdata[index.row()][4].toString()
        return QVariant()
    
    def SetRemarque(self, value):
        self.listdata[self.CurrentIndex.row()][4] = QVariant(value)
        self.listdata[self.CurrentIndex.row()][5] = QVariant(True)
        self.isChanged = True  
          
    def RemoveRow(self, position):
        self.Deleted.append('%i' % self.listdata[position][0].toInt()[0])
        self.listdata = self.listdata[:position] + self.listdata[position + 1:]
        self.removeRow(position)
        self.isChanged = True
    
    def insertRows(self, position, data, rows=1, index=QModelIndex()):
#        hashKey=QImage('../Archives/%s'%data[1]).cacheKey() doesn't work use ImageMagick instead
#         doublon=False
#         for i in self.listdata: #traitement trop long
#             if os.system('compare -metric AE ../Archives/%s ../Archives/%s null'%(data[1],i[2].toString()))==0:
#                 doublon=True
#                 break
#         if doublon:
#             os.remove('../Archives/%s'%data[1])
#             os.remove('../Archives/%s'%data[2])
#         else:
        ligne=[QVariant(0),QVariant(data[0]),QVariant(data[1]),QVariant(data[2]),QVariant(),QVariant(True)]
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.listdata.append(ligne)
        self.endInsertRows()
        self.isChanged=True
#        return doublon
    
    def Save(self, idAnalyse): 
        Myrequest = Request('ResultatAnalyse')
        if not self.isChanged:
            return
        for i in self.Deleted:
            Myrequest.Delete([Myrequest.Fields[0].Name, i])
        for i in self.listdata:
            if not i[5].toBool():
                continue  # Not modified
            values = [i[0], QVariant(idAnalyse), None,None, None, i[1],i[3],i[2],i[4],QVariant(0)]
            (err, values) = Myrequest.ValidData(values)
            if len(err) == 0:
                error = Myrequest.Save(values)
                if not error.isValid():
                    return error
            else:
                print 'Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err))
                return QSqlError('','Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err)))   

class TypeAnalyseDeleguate(QItemDelegate):   
    def setEditorData(self,editor,index):
        if type(editor)==Mywidgets.MyComboBox:
            value = index.model().data(index, Qt.DisplayRole)
            if not value.isNull():
                comboindex=editor.model().GetIndex(value)
            else:
                comboindex=0
            editor.setCurrentIndex(comboindex)
        elif type(editor)==QDateTimeEdit:
            value = index.model().data(index, Qt.DisplayRole).toDateTime()
            editor.setDateTime(value)
        else:
            value=index.model().data(index,Qt.DisplayRole).toString()
            editor.setText(value)
             
    def setModelData(self,editor,model,index):
#        print type(editor)
        if type(editor)==Mywidgets.MyComboBox:
            model.setData(index, QVariant(editor.Getid()))
        elif type(editor)==QDateTimeEdit:    
            model.setData(index,QVariant(editor.dateTime()))
        elif type(editor)==MyPlainTextEdit:
            model.setData(index,editor.toPlainText())
        else:
            model.setData(index,editor.text())

# class Analyses(QAbstractListModel): #=>MyComboModel
#     def __init__(self, idAnimal, parent=None, *args): 
#         QAbstractListModel.__init__(self, parent, *args) 
#         self.Myrequest = Request()
#         self.listdata = self.Myrequest.GetLines('CALL GetAnalysesAnimal(%i)' % idAnimal)
#  
#     def rowCount(self, parent=QModelIndex()): 
#         return len(self.listdata) 
#     
#     def data(self, index, role): 
#         if index.isValid() and role == Qt.DisplayRole:
#             return QVariant(self.listdata[index.row()][1])
#         elif index.isValid() and role == Qt.UserRole:
#             return QVariant(self.listdata[index.row()][0])
#         elif index.isValid() and role == Qt.ToolTipRole:
#             return QVariant(self.listdata[index.row()][3])
#         else: 
#             return QVariant()
        
#debug only        
def Print(self,List,index=0):
    for i in List[index]:
        try:
            print i.toString()
        except:
            print i  
             
if __name__ == '__main__':
    db = QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName (config.host)
    db.setUserName (config.user)
    db.setPassword (config.password)
    db.setDatabaseName(config.database)
    if not db.open():
        print 'connection impossible'
    MyAnalyse = Analyse(db, 'Analyse')
    MyAnalyse.Print()
