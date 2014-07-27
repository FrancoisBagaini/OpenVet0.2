# -*- coding: utf8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtSql import *

class DBase:
    def __init__(self):
        self.Base=None
        self.errConnection=None
        self.Connection()
        
        
    def Connection(self):
        self.Base = QSqlDatabase.addDatabase("QMYSQL")
        self.Base.setHostName ( 'localhost' )
        self.Base.setUserName ( 'root' )
        self.Base.setPassword ( 'horizons' )
        self.Base.setDatabaseName("Opencompta")
        if not self.Base.open():
            self.errConnection=True
        else:
            self.errConnection=False
    
class Request(QSqlQuery):
    def __init__(self,table=None):
        QSqlQuery.__init__(self)
        self.res=None
        self.Table=table
        self.Fields=None
        self.lastID=None
        if not table is None:
            self.GetFields()
            self.FieldsName=[i.Name for i in self.Fields]
        
    def SetTable(self,table):
        self.Table=table
        
    def Execute(self,request):
        self.exec_(request)
        return self.lastError()
        
    def GetInt(self,request,index):
        self.res=None
        self.exec_(request)
        self.next()
        if self.value(index).toInt()[1]:
            self.res=self.value(index).toInt()[0]
        return self.res  
    
    def GetInts(self,request,index):
        self.res=[]
        self.exec_(request)
        while self.next():
            if self.value(index).toInt()[1]:
                self.res.append(self.value(index).toInt()[0])
        if len(self.res)==0:
            self.res=None
        return self.res

    def GetString(self,request,index):
        self.res=None
        self.exec_(request)
        self.next()
        self.res=QString(self.value(index))
        return self.res  
    
    def GetStrings(self,request,index):
        self.res=[]
        self.exec_(request)
        while self.next():
            self.res.append(self.value(index).toString())
        if len(self.res)==0:
            self.res=None
        return self.res
    
    def GetStringList(self,request,index): 
        self.res=QStringList()
        self.exec_(request)
        while self.next():
            self.res<<self.value(index).toString()
        if len(self.res)==0:
            self.res=None
        return self.res
         
    def GetidStrings(self,request,index):
        self.res=[]
        self.exec_(request)
        while self.next():
            self.res.append([self.value(index[0]).toInt()[0],self.value(index[1]).toString()])
        return self.res
    
    def GetLineTable(self,id):
        self.res=[]
        self.exec_("SELECT * FROM %s WHERE id%s=%i"%(self.Table,self.Table,id))
        self.next()
        if self.isValid():
            for i in range(self.record().count()):
                self.res.append(self.value(i))                          
        if len(self.res)==1:
            self.res=None
        return self.res
    
    def GetComboList(self,request,firstField=None):
        #QVariant(Id),QString(Libele),QString(Remarque),QVariant(CodeColor)
        if firstField is None:
            self.res=[]
        else:
            self.res=[[QVariant(0),QString(firstField),QString(''),QVariant(0)]]
        self.exec_(request)
        while self.next():
            if self.record().count()>3:
                self.res.append([self.value(0),self.value(1).toString(),self.value(2).toString(),self.value(3)])
            else:
                self.res.append([self.value(0),self.value(1).toString(),self.value(2).toString(),QVariant(0)])
        return self.res
    
    def GetLines(self,request):
        self.res=[]
#        query=QSqlQuery()
        self.exec_(request)
        while self.next():
            tmp=[]
            for i in range(self.record().count()):
                tmp.append(self.value(i))#.toString()
            self.res.append(tmp)
        return self.res

    def GetLine(self,request):
        self.res=[]
        self.exec_(request)
        self.next()
        if self.isValid():
            for i in range(self.record().count()):
                self.res.append(self.value(i).toString())                          
#            self.res=[self.value(i) for i in range(self.size())]
        if len(self.res)==0:
            self.res=None
        return self.res
    
    def GetFields(self,table=None):
        if not table is None:
            self.Table=table
        self.Fields=[]
        self.exec_("SHOW COLUMNS FROM %s"%self.Table)
        while self.next():
            self.Fields.append(Field(self))
        return self.Fields
            
    def GetFieldIndex(self,name):
        for i in range(len(self.Fields)):
            if self.Fields[0].Name==name:
                return i
        return -1
    
    def ValidData(self,values,fields=None): #values are QString or QVariant
        err=[]
        newvalues=[]
        if fields is None:
            fields=self.Fields
        if len(values)!=len(fields):
            return ([u'Nombre de valeurs erroné'],None)
        for i,j in zip(values,fields):
            if i is None:
                if j.Null:
                    newvalues.append('NULL')
                else:
                    err.append(j.Name)
                continue
            if 'int' in j.Type:
                if i.toInt()[1]:
                    newvalues.append('%i'%i.toInt()[0])
                else:
                    err.append(j.Name)
            if 'decimal' in j.Type or 'float' in j.Type:
                if i.toFloat()[1]:
                    newvalues.append('%.2f'%i.toFloat()[0])
                else:
                    err.append(j.Name)
            if 'date' in j.Type:
                if i.toDate()[1]:
                    newvalues.append('\"%s"'%i.toString('yyyy-MM-dd'))
                else:
                    err.append(j.Name)
            if 'datetime' in j.Type:
                if i.toDateTime()[1]:
                    newvalues.append('\"%s"'%i.toString('yyyy-MM-dd : hh:mm'))
                else:
                    err.append(j.Name)
            if 'varchar' in j.Type or 'text' in j.Type:
                if i.toString().isEmpty():
                    if j.Null:
                        newvalues.append('NULL')
                    else:
                        err.append(j.Name)
                else:
                    if i.toString().size()<=j.Maxlength:
                        newvalues.append(u'\"%s"'%i.toString())
                    else:
                        err.append(j.Name)
        return (err,newvalues)
                
    def Delete_Act(self,id):
        self.exec_("CALL DeleteItemTable(%i,\"%s\")"%(id,self.Table))
        return self.lastError()
    
    def Delete(self,ids):
        self.exec_("DELETE FROM %s WHERE %s"%(self.Table,'='.join(ids)))
        return self.lastError()
    
    def Save(self,values,fields=None):
        if values[0]=='0':
            return self.Add(values)
        else:
            if fields is None:
                fields=self.FieldsName
            return self.Update(fields,values)
    
    def Add(self,values):
        values=','.join(values)
        if not self.Table is None:
            self.exec_("INSERT INTO %s VALUES (%s)"%(self.Table,values))
            self.lastID=self.lastInsertId()
            return self.lastError()
        else:
            return QSqlError('','Table non renseignée.')

    def Update(self,fields,values):
        idtable='='.join(zip(fields,values)[0])
        sets=','.join(['='.join(i) for i in zip(fields,values)[1:]])
        if not self.Table is None:
            self.exec_("UPDATE %s SET %s WHERE %s"%(self.Table,sets,idtable))
            return self.lastError()

class Field:
    def __init__(self,query):
        self.Name=str(query.value(0).toString())
        tmp=str(query.value(1).toString())
        self.Maxlength=None
        if tmp.count('(') and 'varchar' not in tmp:
            self.Type=tmp[:tmp.index('(')]
        elif 'varchar' in tmp:
            self.Type=tmp
            self.Maxlength=int(tmp[tmp.index('(')+1:tmp.index(')')])
        elif 'text' in tmp:
            self.Type='text'
            if tmp=='text':
                self.Maxlength=65535
            elif 'tinytext'==tmp:   #To avoid
                self.Maxlength=255
            elif 'mediumtext'==tmp: #To avoid
                self.Maxlength=16777216    
        else:
            self.Type=tmp
        self.Null=str(query.value(2).toString())=='YES'
        
        
                