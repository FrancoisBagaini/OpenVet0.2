#!/usr/bin/env python
# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyComboBox(QComboBox):
	def __init__(self,parent=None):
		super(MyComboBox,self).__init__(parent)
		self.completer=None
		
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

	def SetCompleter(self):
		self.setFocusPolicy(Qt.StrongFocus)
		self.setEditable(True)
		# add a filter model to filter matching items
		self.pFilterModel = QSortFilterProxyModel(self)
		self.pFilterModel.setSourceModel(self.model())
		self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)	#Bug filtering is CaseSensitive
		self.completer = QCompleter(self.pFilterModel, self)
		# always show all (filtered) completions
		self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)#reg
		self.setCompleter(self.completer)
		# connect signals
		self.connect(self,SIGNAL('editTextChanged(QString)'),self.OnUpdateCompleter)
		self.connect(self.completer,SIGNAL('activated(QString)'),self.OnCompleterActivated)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.connect(self,SIGNAL('customContextMenuRequested(const QPoint&)'), self.OnPopup)

	def OnUpdateCompleter(self,text):
		text='^'+text
		self.pFilterModel.setFilterRegExp(text)
	
	def OnCompleterActivated(self, text):
		if text:
			index = self.findText(text)
			self.setCurrentIndex(index)
			self.emit(SIGNAL("activated(int)"),index)

	# on model change, update the models of the filter and completer as well 
	def setModel(self, model,isCompleter=False):
		super(MyComboBox,self).setModel(model)
		if self.count()<10:
			self.showPopup ()
		else:
			self.hidePopup ()
		if isCompleter:
			self.pFilterModel.setSourceModel(model)
			self.completer.setModel(self.pFilterModel)
			
	def SetPopup(self,inlist):
		self.Popup=QMenu()
		self.Popup.setStyleSheet("QMenu {background-color: rgb(0,0,94);color: rgb(188,255,2);border: 1px solid #000;}")
		self.items=[]
		for i in inlist:
			action=self.Popup.addAction(i[0].toString())
			action.setToolTip(i[1].toString())
			if len(i)>2:
				action.setData(QVariant(i[2:]))
			action.setCheckable(True)
			self.items.append(action)
			self.connect(action,SIGNAL("triggered(bool)"),self.OnSelectPopupItem)
	
	def OnPopup(self,point):
		self.Popup.exec_(self.mapToGlobal(QPoint(1,point.y()+8)))

	def OnSelectPopupItem(self,action):
		for j,i in enumerate(self.items):
			if i!=self.sender():
				i.setChecked(False)
			else:
				index=j
		self.SelectionContext=[index].extend(self.sender().data().toPyObject())
		self.emit(SIGNAL("ContextMenuActivated"))		
		
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
		
	def Getid(self):
		return self.model().data(self.currentIndex(),Qt.UserRole).toInt()[0]
	
	def keyReleaseEvent(self,event):
		if event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
			self.emit(SIGNAL("OnEnter"))
		else:
			QTableWidget.keyPressEvent(self,event)
		
	def autoResize(self,varcol):
		#redimentionne avec la colonne varcol étant la plus large possible, sous réserve que les autres colonnes affichent les données en entier.
		self.resizeColumnsToContents()
		#if verticalSrollBar
		if self.model() is None:
			return
		tot=1+sum([self.columnWidth(i) for i in range(self.model().columnCount()) if i!=varcol])
		if self.verticalScrollBar().isEnabled():
			tot+=18
		self.setColumnWidth(varcol,self.width()-tot)

	def minimumSizeHint(self):
		return QSize(self.size().width(),30+self.horizontalHeader().height())

	def maximumSizeHint(self):
		return QSize(self.size().width(),5*self.rowHeight(0)+self.horizontalHeader().height()+self.horizontalScrollBar().height())
	
	def sizeHint(self):
		height=(self.model().rowCount()+1)*self.rowHeight(0)+self.horizontalHeader().height()
		if not self.horizontalScrollBar().isHidden():
			height+=self.horizontalScrollBar().height()
		return QSize(self.size().width(),height)
	
	def ResizeHeight(self):	
		self.setVisible(False)
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		self.setVisible(True)
#		self.resize(self.sizeHint())
		self.setMinimumHeight(self.minimumSizeHint().height())
		self.setMaximumHeight(min(self.maximumSizeHint().height(),self.sizeHint().height()))
		self.update()
		self.updateGeometry()


class MyTreeView(QTreeView):
	def __init__(self,parent=None):
		super(MyTreeView,self).__init__(parent)
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setUniformRowHeights(True)
		
	def Getid(self):
		return self.currentIndex().data(Qt.UserRole)

		