#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyComboBox(QComboBox):
	def __init__(self,parent=None):
		super(MyComboBox,self).__init__(parent)
#	def focusInEvent(self, event):
#			self.emit(QtCore.SIGNAL("focusIn"))
#			QtGui.QWidget.focusInEvent(self, event)
#	def mousePressEvent(self, event):
#			self.emit(QtCore.SIGNAL("focusIn"))
#			QtGui.QWidget.mousePressEvent(self, event)

	def keyPressEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QComboBox.keyPressEvent(self,event)
					
	def GetData(self):
		value=self.itemData(self.currentIndex()).toInt()
		if value[1]:
			idata=value[0]
		else:
			idata=None
			print 'Erreur d\'index: %s,\" %s\"'%(self.objectName(),self.currentText())
		return idata
	
	def Setid(self,idTable):
		index=[i for i,j in enumerate(self.model().listdata) if idTable==j[0].toInt()[0]]
		if len(index)==0:
			self.setCurrentIndex(0)
		else:
			self.setCurrentIndex(index[0])
	
	def Getid(self):
		return self.itemData(self.currentIndex(),Qt.UserRole).toInt()[0]
	
	def GetRemarque(self):
		return self.itemData(self.currentIndex(),Qt.ToolTipRole).toString()

	def GetProperty(self,index):
		return self.itemData(self.currentIndex(),33+index)

	def GetDeleted(self):
		return self.itemData(self.currentIndex(),33)


class MyCompleter(QComboBox):
	def __init__(self,parent=None):
		super(MyCompleter,self).__init__(parent)
		self.setFocusPolicy(Qt.StrongFocus)
		self.setEditable(True)
 		# add a filter model to filter matching items
 		self.pFilterModel = QSortFilterProxyModel(self)
 		self.pFilterModel.setSourceModel(self.model())
 		self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)	#Bug filtering is CaseSensitive
		self.completer = QCompleter(self.pFilterModel, self)
		# always show all (filtered) completions
		self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self.setCompleter(self.completer)
		# connect signals
		self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
		self.completer.activated.connect(self.on_completer_activated)

	def on_completer_activated(self, text):
		if text:
			index = self.findText(text)
			self.setCurrentIndex(index)
			self.activated[str].emit(self.itemText(index))

	# on model change, update the models of the filter and completer as well 
	def setModel(self, model):
		super(MyCompleter, self).setModel(model)
 		self.pFilterModel.setSourceModel(model)
 		self.completer.setModel(self.pFilterModel)

	def keyPressEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QComboBox.keyPressEvent(self,event)


class MyTableWidget(QTableWidget):
	def __init__(self,parent=None):
		super(MyTableWidget,self).__init__(parent)
		
	def keyReleaseEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QTableWidget.keyPressEvent(self,event)


class MyPlainTextEdit(QPlainTextEdit):
	def __init__(self,parent=None):
		super(MyPlainTextEdit,self).__init__(parent)
		self.MaxLength=0
		self.textChanged.connect(self.OnLimitLength)
		
	def SetMaxLength(self,length):
		self.MaxLength=length
		
	def OnLimitLength(self):
		if self.MaxLength==0:
			return
		text=self.toPlainText()
		if text.length()>self.MaxLength:
			self.setPlainText(text.remove(text.length()-1,1))
			self.moveCursor(QTextCursor.End)
	
	def setText(self,value):
		self.setPlainText(value)
			
class MyTableView(QTableView):
	def __init__(self,parent=None):
		super(MyTableView,self).__init__(parent)
	
	def keyReleaseEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QTableWidget.keyPressEvent(self,event)
		
	def autoResize(self,varcol):
		#redimentionne avec la colonne varcol étant la plus large possible, sous réserve que les autres colonnes affichent les données en entier.
		self.resizeColumnsToContents()
		if self.model() is None:
			return
		tot=6+sum([self.columnWidth(i) for i in range(self.model().columnCount()) if i!=varcol])
		self.setColumnWidth(varcol,self.width()-tot)
