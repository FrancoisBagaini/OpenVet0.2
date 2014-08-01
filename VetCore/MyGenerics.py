#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import os
import sys
import config
from DBase import Request

class MyComboModel(QAbstractListModel):
    def __init__(self, parentwidget,routine=None,firstField=None):
        QAbstractListModel.__init__(self, parent=None)
        self.MyRequest=Request()
        self.error=None
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
        return 4
    
    def data(self, index, role): 
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()][1])
        elif role == Qt.UserRole:
            return QVariant(self.listdata[index.row()][0])
        elif role == Qt.ToolTipRole:
            return QVariant(self.listdata[index.row()][2])
        elif role == Qt.BackgroundColorRole: #Qt.ForegroundRole BUG in pyqt4 with ubuntu 10.04 test 12.04
            return QColor(Qt.red)
        else: 
            return QVariant()
        
    def Print(self):
        for i in self.listdata:
            print '%i:%s (%s)'%(i[0].toInt()[0],i[1],i[2].toString())
            
# def insert(data):

class MyForm(QDialog):
    def __init__(self,title,data,parent=None):
        QDialog.__init__(self,parent)
        #data: libélé,typewidget,maxlen/routine
        self.setWindowTitle(title)
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.labels=[]
        self.fields=[]
        for index,i in enumerate(data):
            label = QLabel('%s :'%i[0],self)
            self.labels.append(label)
            if i[1]==1: #LineEdit
                field = QLineEdit(self)
                field.setMaxLength(i[2])
                self.fields.append(field)
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
    
    def SetModel(self,model,maplist):
        if len(self.fields)!=len(maplist):
            return False
        self.MyModel=model
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setOrientation(Qt.Horizontal)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.MyModel)
        self.MyDelegate=GenericDelegate(self)
        for i in maplist:
            self.MyDelegate.insertFieldDelegate(i,self.MyModel.Fields) 
        self.mapper.setItemDelegate(self.MyDelegate)
#        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        for i,j in zip(self.fields,maplist):
            self.mapper.addMapping(i, j)
        self.mapper.toFirst()
        return True
            
    def OnDelete(self):
        if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de vouloir effacer cet élément?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.Yes:
            self.MyModel.Delete(self.mapper.currentIndex())
            self.mapper.submit()
            self.accept()
    
    def OnValid(self):  #surcharger ou valider avec DBase
#         if self.lineEdit_Unite.text().isEmpty():
#             QMessageBox.warning(self,u"Alerte OpenVet",'Le champ Unité n\'est pas renseigné', QMessageBox.Ok | QMessageBox.Default)
#             return
#         if (not self.checkBox_isConcentration.isChecked() and self.isConcentration)==True:
#             if QMessageBox.question(self,'OpenVet',u'Etes-vous certain de ne pas attribuer cette unité à une concentration?',QMessageBox.Yes|QMessageBox.Default,QMessageBox.No)==QMessageBox.No:
#                 return
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

        
class MyTable(QSqlTableModel):
    def __init__(self, table,idTable,parent=None, *args):
        QSqlTableModel.__init__(self, parent, *args)
        self.Table=table
        self.setTable(table)
        self.setFilter('id%s=%i'%(table,idTable))
        self.select()
        self.fields=[]
        self.NbFields=0
        self.MyRequest=Request(table)
        self.GetFields()
        
    def GetFields(self):
        self.Fields=self.MyRequest.GetFields()
        self.NbFields=len(self.Fields)
         
    def SetNew(self,new):
        if self.NbFields!=len(new):
            return False
        else:
            self.Newfields=new
            return True
        
    def Setid(self,idTable):
        self.setFilter('id%s=%i'%(self.Table,idTable))
       
    def New(self):
        self.setFilter('id%s=0'%self.Table)
        self.insertRow(0)
        for index,i in enumerate(self.Newfields):
            self.setData(self.index(0, index), QVariant(i), Qt.EditRole)
        
    def Delete(self,row):
        id=self.record(row).value(0).toInt()[0]
        self.removeRow(row)
        self.MyRequest.Delete_Act(id)
        
    def Update(self,index):
        rec=self.record(0)
        self.NbFields=rec.count()
        values=[]
        for i in range(self.NbFields):
            value=rec.value(i)
            if value.isNull():
                value=None
            values.append(value)
        (err, values) =self.MyRequest.ValidData(values, self.Fields)
        if len(err) == 0:
            error = self.MyRequest.Save(values)
        if error.isValid():
            return error
        #self.submitAll()
 
        
class MyModel(QAbstractListModel):
    def __init__(self, table,idTable,parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.Table=table
        self.Fields=[]
        self.NbFields=0
        self.MyRequest=Request(table)
        self.GetFields()
        self.listdata=self.MyRequest.GetLineTable(idTable)
        self.dirty=False
        
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
            return False
        else:
            self.Newfields=[QVariant(i) for i in new]
            return True
        
    def Setid(self,idTable):
        self.listdata=self.MyRequest.GetLineTable(idTable)
       
    def New(self):
        self.listdata=self.Newfields
        
    def Delete(self,row):
        if self.CheckActif:
            self.MyRequest.Delete_Act(self.listdata[0])
        else:
            self.MyRequest.Delete(self.listdata[0])
        
    def Update(self,index):
        values=[]
        for i in range(self.NbFields):
            value=self.listdata[i]
            if value.isNull():
                value=None
            values.append(value)
        (err, values) =self.MyRequest.ValidData(values, self.Fields)
        if len(err) == 0:
            error = self.MyRequest.Save(values)
        if error.isValid():
            return error
 
        
class GenericDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}

    def insertColumnDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate

    def insertFieldDelegate(self,column,fields):
        if fields[column].Type=='int':
            self.insertColumnDelegate(column, IntegerColumnDelegate())
        elif fields[column].Type=='Text' or 'varchar':
            self.insertColumnDelegate(column, PlainTextColumnDelegate())
        elif 'decimal' in fields[column].Type:
            NbDecimales=int(fields[column].Type[fields[column].Type.index(',')+1:fields[column].Type.index(')')])
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
        model.setData(index, QVariant(editor.text()))

class MyError():
    def __init__(self,parent,error):
        display=QErrorMessage(parent)
        display.showMessage(error)
        