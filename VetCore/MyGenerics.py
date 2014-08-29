#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import os
import sys
import config
import Core
from DBase import Request
from Mywidgets import *

class MyComboModel(QAbstractListModel):     #Convient aussi pour QListView
    def __init__(self, parentwidget,routine=None,firstField=None):
        QAbstractListModel.__init__(self, parent=None)
        self.ParentWidget=parentwidget
        self.MyRequest=Request()
        self.error=None
        self.isEditable=False
        self.dirty=False
        if routine is None:
            self.Routine=QString('')
        else:
            self.Routine=routine
            self.listdata = self.MyRequest.GetComboList('CALL %s'%self.Routine,firstField )
            if self.MyRequest.lastError().isValid():
                self.error=self.MyRequest.lastError().text()
                MyError(parentwidget,self.error)
              
    def Set(self,routine=None,firstField=None):
        if not routine is None:
            self.Routine=routine
        self.listdata = self.MyRequest.GetComboList('CALL %s'%self.Routine,firstField )
        if self.MyRequest.lastError().isValid():
            self.error=self.MyRequest.lastError().text()
                
    def rowCount(self,parent=QModelIndex()): 
        return len(self.listdata)
     
    def columnCount(self, index=QModelIndex()):
        try:
            return len(self.listdata[0])
        except:
            return 0
    
    def data(self, index, role): 
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()][1])
        if role == Qt.EditRole:
            return QVariant(self.listdata[index.row()][1])
        elif role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif role == Qt.ToolTipRole:
            return QVariant(Core.Multiline(self.listdata[index.row()][2]))
        elif role == Qt.ForegroundRole: #Qt.ForegroundRole BUG in pyqt4 with ubuntu 10.04 TODO: test 12.04
            color=self.listdata[index.row()][3].toInt()[0]
            if color>0:
                if color==6:
                    return(QColor(Qt.lightGray))
                elif color==7:
                    return(QColor(Qt.red))
                elif color==8:
                    return(QColor(Qt.green))
        elif role == 33:    #isDeleted
            return QVariant(self.listdata[index.row()][4])
        elif role > 33:    #UserProperty
            return QVariant(self.listdata[index.row()][4+role-33])
        else: 
            return QVariant()
    
    def setData(self,index,value,role=Qt.EditRole):
        if not index.isValid():
            return False
        value=QVariant(value)
        if role == Qt.EditRole:
            self.listdata[index.row()][1]=value.toString()
        elif role == Qt.UserRole:
            self.listdata[index.row()][0]=value
        elif role == Qt.ToolTipRole:
            self.listdata[index.row()][2]=value.toString()
        elif role == Qt.ForegroundRole:
            self.listdata[index.row()][3]=value
        elif role == 33:    #isDeleted
            self.listdata[index.row()][4]=value
        elif role > 33:    #UserProperty
            self.listdata[index.row()][4+role-33]=value
        else: 
            return False
        if role!=33:
            self.dirty = True
            self.SignId(index)
        else:
            self.SignId(index,False)
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index,index)
        return True
        
    def flags(self,index):
        if not index.isValid() or not self.isEditable:
            return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        return Qt.ItemFlags(QAbstractListModel.flags(self,index)|Qt.ItemIsEditable)
          
    def Extend(self,value):  #for more user data
        for i in self.listdata:
            i.append(QVariant(value))
        
    def NewLine(self,data):
        for i,j in enumerate(data):
            if i in [1,2]:
                j=QString(j)
            else:
                data[i]=QVariant(j)
        row=self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self.listdata.append(data)
        self.endInsertRows()
        self.dirty = True
           
    def GetIndex(self,currentid):
        res=[i for i in self.listdata if i[0]==currentid]
        if len(res)==0:
            MyError(self.ParentWidget,u'L\'identifiant %i est absent de la liste retournée par: %s'%(currentid.toInt()[0],self.Routine))
        return self.listdata.index(res[0])
           
    def SignId(self,index,neg=True):
        if neg:
            self.listdata[index.row()][0]=QVariant(-abs(self.listdata[index.row()][0].toInt()[0]))
        else:
            self.listdata[index.row()][0]=QVariant(abs(self.listdata[index.row()][0].toInt()[0]))
            
    def EditItem(self,values,table,maplist,idindex,delindex,parent):
        values[idindex]=QVariant(abs(values[idindex].toInt()[0]))
        model=MyModel(table,0,parent)
        model.SetNew([values[j] for j in maplist])
        model.New()
        model.Update()
        return model.lastid
#         if values[idindex].toInt()[0]==0:
#             [idindex]=model.lastid
            
    def DeleteItem(self,table,id,parent):
        model=MyModel(table,abs(id),parent)
        model.Delete()
        
    def Update(self,table,maplist,parent,idindex=0,delindex=4):
        if not self.dirty:
                return
        for i in self.listdata:
            id=i[idindex].toInt()[0]
            if id<=0 and not i[delindex].toBool():
                self.EditItem(i,table,maplist,idindex,delindex,parent)
            elif i[delindex].toBool() and id!=0:
                self.DeleteItem(table,abs(id),parent)
            
    def UpdateRelational(self,table,maplist,tableref,maplistref,idref,delref,parent):
        if not self.dirty:
            return
        for i in self.listdata:
            idtable=i[0].toInt()[0]
            idtableref=i[idref].toInt()[0]
            isdeltable=i[4].toBool()
            isdeltableref=i[delref].toBool()
            if idtable <=0 and not isdeltable:
                lastid=self.EditItem(i,table,maplist,0,4,parent)
                if idtable==0:
                    i[0]=lastid
                if idtableref==0 and not isdeltableref:
                    self.EditItem(i,tableref,maplistref,idref,delref,parent)
            elif isdeltableref and idtableref!=0:
                self.DeleteItem(tableref,abs(idtableref),parent)
                if isdeltable and idtable!=0:
                    self.DeleteItem(table,abs(idtable),parent)
                    
    def Fdata(self,col,vtype=None,debug=False):     #TODO: Move in Core Fdata(self,value,vtype=None,debug=False)
        value=self.listdata[col]
        if vtype is None:
            vtype=value.typeName()
        if value.isNull():
            if debug:
                return 'NULL'
            else:
                return QString('')
        elif vtype=='QDate':
            return value.toDate().toString('dd/MM/yyyy')
        elif vtype=='QDateTime':
            return value.toDateTime().toString('dd/MM/yyyy hh:mm')
        elif vtype in ['int','qlonglong']:
            return value.toInt()[0]
        elif vtype=='QString':
            return value.toString()
        elif vtype=='bool':
            return value.toBool()
        else:
            return u'indeterminé'
        
    def Print(self):
        for i in range(self.NbFields):
            value=self.listdata[i]
            if value.isNull():
                value=None
            print '%i. %s : %s'%((i+1),self.Fields[i].Name,str(self.Fdata(i,None,True)))  
                  
#     def Print(self): 
#         for i in self.listdata:
#             print '%i:%s (%s)'%(i[0].toInt()[0],i[1],i[2].toString())

            
# class MyTableModel(QAbstractTableModel):
#     def __init__(self, idAnalyse, parent=None, *args): 
#         QAbstractTableModel.__init__(self, parent, *args)
#         self.Myrequest = Request()
#         self.listdata = self.Myrequest.GetLines('CALL GetResultatParametres(%i)' % idAnalyse)
#         self.Fields
#         
#     def Print(self):
#         for i in range(self.NbFields):
#             value=self.listdata[i]
#             if value.isNull():
#                 value=None
#             print '%i. %s : %s'%((i+1),self.Fields[i].Name,str(self.Fdata(i,None,True)))  
#                  
#     def rowCount(self, parent=QModelIndex()): 
#         return len(self.listdata)
#     
#     def columnCount(self, parent=QModelIndex()):
#         try:
#             return len(self.listdata[0])
#         except:
#             return 0
#     
#     def headerData(self, col, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return QVariant(self.Headers[col])
#         return QVariant()
#     
#     def data(self, index, role): 
#         if index.isValid() and role == Qt.DisplayRole:
#             if index.column() in [2, 4, 5]:
#                 if self.listdata[index.row()][index.column()].toFloat()[1]:
#                     return QVariant('%.2f' % self.listdata[index.row()][index.column()].toFloat()[0])
#                 else:
#                     return QVariant()            
#             else:
#                 return QVariant(self.listdata[index.row()][index.column()])
#         elif index.isValid() and role == Qt.TextAlignmentRole:
#             if index.column() > 1:
#                 return QVariant(int(Qt.AlignRight | Qt.AlignCenter))
#         elif index.isValid() and role == Qt.ToolTipRole:
#             return self.listdata[index.row()][6]
#         elif index.isValid() and index.column() == 2 and role == Qt.TextColorRole:
#             if not self.listdata[index.row()][7].toBool():
#                 return QVariant()
#             lmax = self.listdata[index.row()][2].toFloat() > self.listdata[index.row()][5].toFloat()
#             lmin = self.listdata[index.row()][2].toFloat() < self.listdata[index.row()][4].toFloat()
#             if lmax or lmin:
#                 return QVariant(QColor(Qt.red))
#             else:
#                 return QVariant()
#         else: 
#             return QVariant()
#         
#     def flags(self, index):
#         if index.isValid() and index.column() == 2:
#             return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
#         else:
#             return Qt.ItemIsEnabled
#         
#     def setData(self, index, value, role=Qt.EditRole):
#         if index.isValid() and index.row() < self.rowCount():
#             self.CurrentIndex = index
#             self.listdata[index.row()][2] = value.toString()    
#             self.listdata[index.row()][9] = True   
#             self.isChanged = True
#             self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
#             return True
#         return False
#     
#     def removeRows(self, position, rows=1, index=QModelIndex()):
#         if self.rowCount()==0:
#             return False
#         self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
#         self.Deleted.append('%i' % self.listdata[position][0].toInt()[0])
#         self.listdata = self.listdata[:position] + self.listdata[position + rows:]
#         self.endRemoveRows()
#         self.isChanged = True
#         return True
#     
#     def insertRows(self, position, choix, rows=1, index=QModelIndex()):
#         valid = True
#         newparametre = self.Parametres.GetParametre(choix)
#         if not self.isExist(newparametre[1]):
#             self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
#             self.listdata.append(newparametre)
#             self.endInsertRows()
#             self.isChanged = True
#             #resizeto contents
#         else:
#             valid = False  
#         return valid
#             
#     def SetModel(self,Parametres):
#         valid = False
#         if self.rowCount()>0:
#             self.removeRows(0,self.rowCount())
#         for i in range(Parametres.rowCount()):
#             valid = True
#             newparametre = Parametres.GetParametre(i)
#             if not self.isExist(newparametre[1]):
#                 self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
#                 self.listdata.append(newparametre)
#                 self.endInsertRows()
#             else:
#                 valid = False
#         self.isChanged = True
#         return valid
#     
#     def Save(self, idAnalyse): 
#         Myrequest = Request('ResultatAnalyse')  
#         for i in self.Deleted:
#             Myrequest.Delete([Myrequest.Fields[0].Name, i])
#         for i in self.listdata:
#             if not i[9]:
#                 continue  # Not modified
#             values = [i[0], QVariant(idAnalyse),i[8]]
#             if i[2].toFloat()[1]:
#                 values.extend([i[2], None, None,None,None, i[6]])
#             else:
#                 values.extend([None, i[2], None,None,None,i[6]])
#             (err, values) = Myrequest.ValidData(values)
#             if len(err) == 0:
#                 # TODO Myrequest.Save(values,[3,4,9]) if update  
#                 error = Myrequest.Save(values)
#                 if not error.isValid():
#                     return error
#             else:
#                 print 'Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err))
#                 return QSqlError('','Erreur dans la table %s pour le(s) champ(s): %s' % (Myrequest.Table, ','.join(err)))   

        
# class MyTable(QSqlTableModel):
#     def __init__(self, table,idTable,parent=None, *args):
#         QSqlTableModel.__init__(self, parent, *args)
#         self.Table=table
#         self.setTable(table)
#         self.setFilter('id%s=%i'%(table,idTable))
#         self.select()
#         self.fields=[]
#         self.NbFields=0
#         self.MyRequest=Request(table)
#         self.GetFields()
#         
#     def GetFields(self):
#         self.Fields=self.MyRequest.GetFields()
#         self.NbFields=len(self.Fields)
#          
#     def SetNew(self,new):
#         if self.NbFields!=len(new):
#             return False
#         else:
#             self.Newfields=new
#             return True
#         
#     def Setid(self,idTable):
#         self.setFilter('id%s=%i'%(self.Table,idTable))
#        
#     def New(self):
#         self.setFilter('id%s=0'%self.Table)
#         self.insertRow(0)
#         for index,i in enumerate(self.Newfields):
#             self.setData(self.index(0, index), QVariant(i), Qt.EditRole)
#         
#     def Delete(self,row):
#         id=self.record(row).value(0).toInt()[0]
#         self.removeRow(row)
#         self.MyRequest.Delete_Act(id)
#         
#     def Update(self,index):
#         rec=self.record(0)
#         self.NbFields=rec.count()
#         values=[]
#         for i in range(self.NbFields):
#             value=rec.value(i)
#             if value.isNull():
#                 value=None
#             values.append(value)
#         (err, values) =self.MyRequest.ValidData(values, self.Fields)
#         if len(err) == 0:
#             error = self.MyRequest.Save(values)
#         if error.isValid():
#             return error
#         #self.submitAll()
 
        
class MyModel(QAbstractListModel):
    def __init__(self, table,idTable,parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        if isinstance(idTable,QVariant):
            idTable=idTable.toInt()[0]
        self.Table=table
        self.Fields=[]
        self.NbFields=0
        self.ParentWidget=parent
        self.MyRequest=Request(table,self.ParentWidget)
        self.GetFields()
        self.listdata=self.MyRequest.GetLineTable(idTable)      
        self.lastid=0
        
    def Print(self):
        for i in range(self.NbFields):
            value=self.listdata[i]
            if value.isNull():
                value=None
            print '%i. %s : %s'%((i+1),self.Fields[i].Name,str(self.Fdata(i,None,True)))
            
    def ExtendData(self,row,extdata):
        #[id,data1,data2,...]
        if extdata[0]==self.listdata[0]:
            self.listdata.extend(extdata[1:])
        else:
            MyError(self.ParentWidget,u'L\'id des données à ajouter ne coorespond pas à l\'id des données déjà présentes')

    def rowCount(self,parent=QModelIndex()):
        return 1
    
    def columnCount(self,parent=QModelIndex()):
        return self.NbFields
    
    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.column()])
        else: 
            return QVariant()
    
    def Fdata(self,col,vtype=None,debug=False):
        value=self.listdata[col]
        if vtype is None:
            vtype=value.typeName()
        if value.isNull():
            if debug:
                return 'NULL'
            else:
                return QString('')
        elif vtype=='QDate':
            return value.toDate().toString('dd/MM/yyyy')
        elif vtype=='QDateTime':
            return value.toDateTime().toString('dd/MM/yyyy hh:mm')
        elif vtype in ['int','qlonglong']:
            return value.toInt()[0]
        elif vtype=='QString':
            return value.toString()
        elif vtype=='bool':
            return value.toBool()
        else:
            return u'indeterminé'
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.row()==0:
            self.listdata[index.column()] = value
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
            return True
        return False   
       
    def GetFields(self):
        self.Fields=self.MyRequest.GetFields()
        self.NbFields=len(self.Fields)
             
    def SetNew(self,new):
        if self.NbFields!=len(new):
            MyError(self.ParentWidget,u'Le vecteur d\'initialisation de %s n\'est pas valide'%self.Table)
            return False
        else:
            self.Newfields=[QVariant(i) for i in new]
            return True
        
    def Setid(self,idTable):
        self.listdata=self.MyRequest.GetLineTable(idTable)
       
    def New(self):
        self.listdata=self.Newfields
    
    def BeginTransaction(self):
        self.MyRequest.driver().beginTransaction()
        
    def CommitTransaction(self):
        self.MyRequest.driver().commitTransaction()
          
    def Delete(self):
        self.MyRequest.Delete_Act(self.listdata[0].toInt()[0])
        
    def Update(self,index=0):
        values=[]
        for i in range(self.NbFields):
            value=self.listdata[i]
            if value.isNull():
                value=None
            values.append(value)
#        self.Print()
        (err, values) =self.MyRequest.ValidData(values, self.Fields)
        if len(err) == 0:
            error = self.MyRequest.Save(values)
            if error.isValid():
                return error#TODO :MyError
            else:
                self.lastid=self.MyRequest.lastID
                return self.lastid
 

LINEEDIT,CHECKBOX,PLAINTEXTEDIT,COMBOBOX,LIST,LABELS = range(1,7)

class MyForm(QDialog):
    def __init__(self,title,data,parent=None):
        QDialog.__init__(self,parent)
        #data: libélé,typewidget,maxlen,Qsize,HorizontalGroup
        self.setWindowTitle(title)
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.labels=[]
        self.fields=[]
        self.popMenus=[]
        for index,i in enumerate(data):
            if len(i[0])>0:
                label = QLabel('%s :'%i[0],self)
            else:
                label = QLabel()
            self.labels.append(label)
            if i[1]==1: #LineEdit
                field = QLineEdit(self)
                field.setMaxLength(i[2])
            if i[1]==2: #CheckBox
                field=QCheckBox ('')   
            if i[1]==3: #PlainTextEdit
                field=MyPlainTextEdit(self)
                field.SetMaxLength(i[2])
                field.setMaximumSize(1000,i[3])
            if i[1]==4: #Combobox
                field=MyComboBox(self)
                field.setMaximumSize(1000,27)
            if i[1]==5: #ListView
                field=QListView(self)
                field.setMaximumSize(1000,i[3])
                field.setContextMenuPolicy(Qt.CustomContextMenu)
                self.connect(field,SIGNAL('customContextMenuRequested(const QPoint&)'), self.OnListViewMenu)
                menu = QMenu(field)
                action1=menu.addAction('Supprimer')
                action1.setData(field)
                self.connect(action1,SIGNAL("triggered()"),self.OnList_delete)
                self.popMenus.append(menu)
            self.fields.append(field)
            label.setBuddy(field)
            self.formLayout.setWidget(index, QFormLayout.LabelRole, label)
            self.formLayout.setWidget(index, QFormLayout.FieldRole, field)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QHBoxLayout()
        self.pushButton_Cancel = QPushButton(self)
        self.pushButton_Cancel.setMinimumSize(QSize(0, 27))
        self.pushButton_Cancel.setText(u'Annuler')
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        self.pushButton_Add = QPushButton(self)
        self.pushButton_Add.setMinimumSize(QSize(0, 27))
        self.pushButton_Add.setText(u'Nouveau')
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
        
        self.pushButton_Cancel.clicked.connect(self.OnCancel)
        self.pushButton_Delete.clicked.connect(self.OnDelete)
        self.pushButton_Valid.clicked.connect(self.OnValid)
        self.pushButton_Add.clicked.connect(self.OnNew)

    def InactivateEnter(self):
        self.pushButton_Valid.setAutoDefault(False)
        self.pushButton_Delete.setAutoDefault(False)
        self.pushButton_Add.setAutoDefault(False)
        self.pushButton_Cancel.setAutoDefault(False)
        
    def AddMenuAction(self,widget,label,function):
        for i in self.popMenus:
            if i.parent()==widget:
                i.addAction(label,function)
        
    def OnListViewMenu(self,point):
        for i in self.popMenus:
            if i.parent()==self.sender():
                i.exec_(i.parent().mapToGlobal(point))
                break
            
    def OnList_delete(self): 
        if self.sender().data().toPyObject().model().data(self.sender().data().toPyObject().currentIndex(), 33).toBool():
            isdeleted=False
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(), False, 33)
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(),0,Qt.ForegroundRole)
            QToolTip.showText(QCursor.pos(),u'Elément restauré.')
        else:
            isdeleted=True
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(), True, 33)
            self.sender().data().toPyObject().model().setData(self.sender().data().toPyObject().currentIndex(),6,Qt.ForegroundRole)
            QToolTip.showText(QCursor.pos(),u'Elément marqué pour la suppression.')
        self.sender().data().toPyObject().emit(SIGNAL("isDeleted(int)"),isdeleted)
   
    def SetModel(self,model,maplist):
        self.MyModel=model
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setOrientation(Qt.Horizontal)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyModel)
        self.MyDelegate=GenericDelegate(self)
        for i,j in enumerate(self.fields):
                if maplist.has_key(i):
                    if isinstance(j,QLineEdit):
                        self.MyDelegate.insertFieldDelegate(i+1,self.MyModel.Fields[maplist[i]])
                    elif isinstance(j,QCheckBox):
                        self.MyDelegate.insertColumnDelegate(i+1,CheckboxColumnDelegate())
                    elif isinstance(j,(QPlainTextEdit,MyPlainTextEdit)):  #regrouper avec QLineEdit?
                        self.MyDelegate.insertColumnDelegate(i+1,PlainTextColumnDelegate())              
        self.mapper.setItemDelegate(self.MyDelegate)
        for i,j in enumerate(self.fields):
            if maplist.has_key(i):
                self.mapper.addMapping(j, maplist[i])
        self.mapper.toFirst()
        return True
            
    def OnDelete(self):
        if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de vouloir effacer cet élément?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.Yes:
            self.MyModel.Delete(self.mapper.currentIndex())
            self.mapper.submit()
            self.accept()
    
    def OnValid(self):  #surcharger ou valider avec DBase
        if self.mapper.submit():
            self.MyModel.Update(self.mapper.currentIndex())
            self.accept()
        else:
            if self.mapper.model().lastError().type()==2:
                QMessageBox.warning(self,u"Alerte OpenVet",u'Cette entré constitue un doublon', QMessageBox.Ok | QMessageBox.Default)
            
    def OnNew(self):
        self.MyModel.New()
        self.fields[0].setFocus()
        self.mapper.toFirst()
    
    def OnCancel(self):
        self.close()
        
        
class GenericDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}

    def insertColumnDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate

    def insertFieldDelegate(self,column,field):
        if field.Type=='int':
            self.insertColumnDelegate(column, IntegerColumnDelegate())
        elif field.Type=='id':
            self.insertColumnDelegate(column, ComboboxColumnDelegate())
        elif field.Type=='text' or 'varchar' in field.Type:
            self.insertColumnDelegate(column, PlainTextColumnDelegate())
        elif field.Type=='datetime':
            self.insertColumnDelegate(column, DateColumnDelegate())
        elif 'decimal' in field.Type:
            NbDecimales=int(field.Type[field.Type.index(',')+1:field.Type.index(')')])
            self.insertColumnDelegate(column, FloatColumnDelegate(NbDecimales))

    def removeColumnDelegate(self, column):
        if column in self.delegates:
            del self.delegates[column]


    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QItemDelegate.paint(self, painter, option, index)


    def createEditor(self, parent, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QItemDelegate.createEditor(self, parent, option,index)

    def setEditorData(self, editor, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QItemDelegate.setModelData(self, editor, model, index)


class IntegerColumnDelegate(QItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum


    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return spinbox


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toInt()[0]
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))


class CheckboxColumnDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(CheckboxColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return self

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toBool()
        if value:
            editor.setCheckState(Qt.Checked)
        else:
            editor.setCheckState(Qt.Unchecked)

    def setModelData(self, editor, model, index):
        if editor.checkState():
            model.setData(index, QVariant(True))
        else:
            model.setData(index, QVariant(False))
    
    
class ComboboxColumnDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(ComboboxColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return self

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        if not value.isNull():
            comboindex=editor.model().GetIndex(value)
        else:
            comboindex=0
        editor.setCurrentIndex(comboindex)

    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.Getid()))
        
        
class FloatColumnDelegate(QItemDelegate):

    def __init__(self, minimum=0, maximum=10000, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum


    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        lineedit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return lineedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toFloat()[0]
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))

class DateColumnDelegate(QItemDelegate):

    def __init__(self, minimum=QDate(), maximum=QDate.currentDate(),
                 format="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = QString(format)


    def createEditor(self, parent, option, index):
        dateedit = QDateEdit(parent)
        dateedit.setDateRange(self.minimum, self.maximum)
        dateedit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        dateedit.setDisplayFormat(self.format)
        dateedit.setCalendarPopup(True)
        return dateedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toDate()
        editor.setDate(value)


    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.date()))


class PlainTextColumnDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(PlainTextColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        return lineedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)

    def setModelData(self, editor, model, index):
        if isinstance(editor,(MyPlainTextEdit,QPlainTextEdit)):
            model.setData(index, QVariant(editor.toPlainText()))
        else:
            model.setData(index, QVariant(editor.text()))
            

class MyError():
    def __init__(self,parent,error):
        print error
        display=QErrorMessage(parent)
        display.showMessage(error)
        