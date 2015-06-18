# -*- coding: utf8 -*-
import time
import os
from PyQt4 import QtCore
import Core
from MyGenerics import *
from DBase import *
import ImageQt
from twisted.trial.test import scripttest


class Animal(MyModel):
    def __init__(self,table,idTable,parent):
        MyModel.__init__(self, table, idTable, parent)
        self.Abstract=None
        self.idAnimal=idTable
        
    def GetAbstract(self):
        self.Abstract=self.MyRequest.GetLineModel('CALL GetAnimal_short(%i)'%self.idAnimal)
        return self.Abstract[0].toString()
    
    def GetLastMesure(self):
        ret=self.MyRequest.GetInt('CALL GetLastMesure(%i)'%self.idAnimal)
        if ret is None:
            ret=0
        return ret
    
    def GetLastRelance(self):
        ret=self.MyRequest.GetInt('CALL GetLastRelance(%i)'%self.idAnimal)
        if ret is None:
            ret=0
        return ret
    
class FormAnimal(MyForm):
    def __init__(self,idEspece,data,parent):
        MyForm.__init__(self,u'Animal',data,parent)
        self.idEspece=idEspece
        self.parent=parent
        self.MyRequest = Request()
        self.InactivateEnter()
        self.fields[1].setModel(MyComboModel(self.parent,'GetEspeces()'))
        self.fields[2].setModel(MyComboModel(self.parent,'GetRaces(%i)'%idEspece))
        self.fields[5].setModel(MyComboModel(self.parent,'GetSexes()'))
        self.fields[4].setEditable(True)
        self.fields[2].activated.connect(self.OnUpdateRobes)
        self.EditButtons[0].clicked.connect(self.OnEditEspece)
        self.EditButtons[1].clicked.connect(self.OnEditRace)
    
    def SetMyModel(self,model,maplist):
        self.SetModel(model, maplist)
        self.OnUpdateRobes()
        
    def OnEditEspece(self): 
        new=[0,'','','','',True,False,'']
        model=MyModel('Especes',self.fields[1].Getid(),self)
        if not model.SetNew(new):
            return
        data=[[u'Nom masculin',1,60],[u'Nom féminin',1,60],[u'Adjectif',1,60],[u'Remarque',1,200]]
        form=MyForm(u'Espèce',data,self)
        form.SetModel(model,{0:1,1:2,2:3,3:4})
        if form.exec_():
            self.fields[1].setModel(MyComboModel(self.parent,'GetEspeces()'))
            
    def OnEditRace(self): 
        new=[0,self.fields[1].Getid(),'','',True,'']
        model=MyModel('Race',self.fields[2].Getid(),self)
        if not model.SetNew(new):
            return
        data=[[u'Libélé',1,60],[u'Remarque',1,200]]
        form=MyForm(u'Race',data,self)
        form.SetModel(model,{0:2,1:3})
        if form.exec_():
            self.fields[2].setModel(MyComboModel(self.parent,'GetRaces(%i)'%self.fields[1].Getid()))
            
    def OnUpdateRobes(self):
        text=self.fields[4].currentText()
        self.fields[4].setModel(MyComboModel(self.parent,'GetRobes(%i)'%self.fields[2].Getid()))
        self.fields[4].hidePopup ()
        self.fields[4].setEditText(text)
  
        
class Mesures(MyTextModel):
    def __init__(self, request,parent=None, *args):
        MyTextModel.__init__(self,request)
        self.Age=[i[1].toFloat()[0]for i in self.listdata]  
        self.Poids=[i[2].toFloat()[0]for i in self.listdata]  
        self.Garrot=[i[3].toFloat()[0]for i in self.listdata]
        self.Thorax=[i[4].toFloat()[0]for i in self.listdata]  
          
    def WritePlotDat(self,filename):
        fout=open(filename,'w')
        fout.write('#')
        for i in range(self.NbFields)[1:-2]:
            fout.write(self.Fields[i]+'\t\t')
        fout.write(self.Fields[self.NbFields-2]+'\n')
        for line in self.listdata:
            for col in line[1:-2]:
                fout.write(col.toString()+'\t\t')
            fout.write(line[-2].toString()+'\n')
        fout.close
        
    def GetMax(self,mesure):       
        if sum(mesure)==0:
            return None
        else:
            return max(mesure)
     
    def SetCoordinates(self,Term): 
        if sum(self.Poids)>0:
            self.NbFields+=2
            self.Fields.extend(['poids_x','poids_y'])
            for i in range(len(self.Poids)):  
                Graph_X=(self.Age[i]-Term[0])/(Term[1]-Term[0])
                Graph_Y=(self.Poids[i]-Term[2])/(Term[3]-Term[2])
                Screen_X=Term[4]+Graph_X*(Term[5]-Term[4])
                Screen_Y=Term[6]+Graph_Y*(Term[7]-Term[6])
                self.listdata[i].extend([QVariant(Screen_X),QVariant(Screen_Y)])
        if sum(self.Garrot)>0:
            self.NbFields+=2
            self.Fields.extend(['garrot_x','garrot_y'])
            for i in range(len(self.Poids)):  
                Graph_X=(self.Age[i]-Term[0])/(Term[1]-Term[0])
                Graph_Y=(self.Garrot[i]-Term[2])/(Term[3]-Term[2])
                Screen_X=Term[4]+Graph_X*(Term[5]-Term[4])
                Screen_Y=Term[6]+Graph_Y*(Term[7]-Term[6])
                self.listdata[i].extend([QVariant(Screen_X),QVariant(Screen_Y)])
        if sum(self.Thorax)>0:
            self.NbFields+=2
            self.Fields.extend(['thorax_x','thorax_y'])
            for i in range(len(self.Poids)):  
                Graph_X=(self.Age[i]-Term[0])/(Term[1]-Term[0])
                Graph_Y=(self.Thorax[i]-Term[2])/(Term[3]-Term[2])
                Screen_X=Term[4]+Graph_X*(Term[5]-Term[4])
                Screen_Y=Term[6]+Graph_Y*(Term[7]-Term[6])
                self.listdata[i].extend([QVariant(Screen_X),QVariant(Screen_Y)])

        
class FormMesures(MyForm):
    def __init__(self,idAnimal,data,parent):
        MyForm.__init__(self,u'Poids et Mesures',data,parent)
        self.parent=parent
        self.idAnimal=idAnimal
        self.InactivateEnter()
        
        self.MyMesures=Mesures('CALL GetMesures(%i)'%self.idAnimal)
        self.SetGraph()
        self.fields[0].setScene(self.scene)
        self.scene.selectionChanged.connect(self.OnSelection)
        self.EditButtons[0].setIcon(QIcon('../images/parcourir.png'))
        self.EditButtons[0].clicked.connect(self.OnParcourir)

        
    def SetGraph(self):
        Term=self.MakeCurves()
        self.MyMesures.SetCoordinates(Term)
        img = QImage('../Scripts/poids.gif')
        pixMap = QPixmap.fromImage(img)
        self.scene=QGraphicsScene()
        self.scene.addPixmap(pixMap)
        if sum(self.MyMesures.Poids)>0:
            for i in self.MyMesures.listdata:
                x=i[6].toFloat()[0]
                y=i[7].toFloat()[0]
                obj=self.scene.addEllipse(x-5,480-y-5,10,10, Qt.red,Qt.red)
                obj.setFlag(2)
                tip='(%s ans, %s Kg)\n%s'%(i[1].toString(),i[2].toString(),i[5].toString())
                obj.setToolTip(tip)
                obj.setData(1,i[0].toInt()[0])
        if sum(self.MyMesures.Garrot)>0:
            for i in self.MyMesures.listdata:
                x=i[8].toFloat()[0]
                y=i[9].toFloat()[0]
                obj=self.scene.addEllipse(x-5,480-y-5,10,10, Qt.green,Qt.green)
                obj.setFlag(2)
                tip='(%s ans, %s Kg)\n%s'%(i[1].toString(),i[3].toString(),i[5].toString())
                obj.setToolTip(tip)
                obj.setData(1,i[0].toInt()[0])
        if sum(self.MyMesures.Thorax)>0:
            for i in self.MyMesures.listdata:
                x=i[10].toFloat()[0]
                y=i[11].toFloat()[0]
                obj=self.scene.addEllipse(x-5,480-y-5,10,10, Qt.blue,Qt.blue)
                obj.setFlag(2)
                tip='(%s ans, %s Kg)\n%s'%(i[1].toString(),i[4].toString(),i[5].toString())
                obj.setToolTip(tip)
                obj.setData(1,i[0].toInt()[0])

        
    def MakeCurves(self):
        poids=self.MyMesures.GetMax(self.MyMesures.Poids)
        garrot=self.MyMesures.GetMax(self.MyMesures.Garrot)
        thorax=self.MyMesures.GetMax(self.MyMesures.Thorax)
        if poids is None and garrot is None and thorax is None:
            return
        script='set term gif medium size 640,480\nset output \"poids.gif\"\nset style line 1 lt rgb \"red\" lw 3 pt 6\nset style line 2 lt rgb "green" lw 3 pt 6\n'+\
               'set style line 3 lt rgb "blue" lw 3 pt 6\nset xlabel \"Age (an)\"\n'
        if not poids is None:
            script=script+'set ylabel \"Poids (Kg)\"\nset ytics nomirror\nset yrange [0:%i]\n'%(poids+1)
        if not garrot is None or not thorax is None:
            script=script+'set y2label \"Taille (cm)\"nset y2tics nomirror 5\nset y2range [0:i%]'%(max(garrot,thorax)+1)
        if not poids is None:
            script=script+'plot \"poids.dat\" using 1:2 linetype 1 smooth csplines title \'Poids\' w lines axes x1y1'
            if not garrot is None:
                script=script=',\"poids.dat\" using 1:3 linetype 2 smooth csplines title \'Taille\' w lines axes x1y2'
            if not thorax is None:
                script=script=',\"poids.dat\" using 1:4 linetype 3 smooth csplines title \'Tour de thorax\' w lines axes x1y2'
        else:
            script=script+'plot '
            if not garrot is None:
                script=script='\"poids.dat\" using 1:3 linetype 2 smooth csplines title \'Taille\' w lines axes x1y2'
                if not thorax is None:
                    script=script=',\"poids.dat\" using 1:4 linetype 3 smooth csplines title \'Tour de thorax\' w lines axes x1y2'
            else:
                script=script='\"poids.dat\" using 1:4 linetype 3 smooth csplines title \'Tour de thorax\' w lines axes x1y2'
        script=script+'\nset print \'values.txt\'\nprint GPVAL_X_MIN\nprint GPVAL_X_MAX\nprint GPVAL_Y_MIN\nprint GPVAL_Y_MAX\nprint GPVAL_TERM_XMIN\nprint GPVAL_TERM_XMAX\nprint GPVAL_TERM_YMIN\nprint GPVAL_TERM_YMAX\nset output'
        
        #TODO : courbes de références
        path=os.getcwd()
        os.chdir('../Scripts')
        fout=open('gnuplot.plt','w')
        fout.write(script)
        fout.close()
        self.MyMesures.WritePlotDat('poids.dat')
        os.system('gnuplot gnuplot.plt')
        fin=open('values.txt','r')
        values=[float(i) for i in fin]
        fin.close()
        os.chdir(path)
        return values
    
#     def SetMyModel(self,model,maplist):
#         self.SetModel(model, maplist)

    def OnParcourir(self):
        path=QFileDialog.getOpenFileName(self,u'OpenVet-Choisissez le fichier à importer')
        self.fields[5].setText(path) 
    
    def OnSelection(self):
        sel=self.scene.selectedItems()
        if len(sel)==1:
            idMesure=sel[0].data(1).toInt()[0]
            model=MyModel('PoidsMesure',idMesure,self)
            self.SetModel(model,{1:2,2:3,3:4,4:5,5:6,6:7,7:8})
            
class FormRelances(MyForm):   
    def __init__(self,idAnimal,idClient,data,parent):
        MyForm.__init__(self,u'Relances',data,parent)
        self.parent=parent
        self.idAnimal=idAnimal
        self.idClient=idClient
        self.InactivateEnter()
        self.fields[2].setModel(MyComboModel(self.parent,'GetModelsRelance()'))
        self.fields[0].setModel(MyComboModel(self.parent,'GetRelances(%i)'%self.idAnimal))
        
        menuTable=self.popMenus[0]
        menuTable.clear()
        action=menuTable.addAction('Editer')
        action.setData(self.fields[0])
        self.connect(action,SIGNAL("triggered()"),self.OnEditRelance) 
        
        menuTable=self.popMenus[1]
        menuTable.clear()
        action=menuTable.addAction('Editer')
        action.setData(self.fields[3])
        self.connect(action,SIGNAL("triggered()"),self.OnEditModesRelance) 
        
        self.EditButtons[0].clicked.connect(self.OnEditModelsRelance)


    def SetMyModel(self,model,maplist):
        self.SetModel(model, maplist)
        self.fields[3].setModel(MyComboModel(self.parent,'GetModesRelance(%i)'%self.MyModel.idTable))

        
    def OnEditRelance(self):
        idRelance=self.fields[0].model().data(self.fields[0].currentIndex(),Qt.UserRole).toInt()
        if idRelance[1]:
            model=MyModel('Relance',idRelance[0],self)
            self.SetMyModel(model,{1:3,2:2,4:4,5:5})
        
    
    def OnEditModesRelance(self):
        idModeRelance=self.fields[3].model().data(self.fields[0].currentIndex(),Qt.UserRole).toInt()
        if not idModeRelance[1]:
            return
        new=[0,self.MyModel.idTable,idModeRelance[0],True,True,'']
        model=MyModel('RelanceModeRef',idModeRelance[0],self)
        if not model.SetNew(new):
            return
        data=[[u'Mode de Relance',4],[u'Automatique',2],[u'Mode de Relance actif',2]]
        form=FormModesRelance(self.idClient,data,self)
        form.SetModel(model,{0:2,1:3,2:4})
        if form.exec_():
            self.fields[3].setModel(MyComboModel(self.parent,'GetModesRelance(%i)'%self.MyModel.idTable))
            #Cf OnEditModelsRelance pour mettre a jour current index
    #Attention les modes de relances sont conservées si annuler edition relance
    
    def OnEditModelsRelance(self):
        idModel=self.MyModel.listdata[2].toInt()
        if not idModel[1]:
            return  #id Invalide
        new=[0,'','',None,True,'']
        model=MyModel('ModelRelance',idModel[0],self)
        if not model.SetNew(new):
            return
        data=[[u'Type de Relance',1,45],[u'texte',3,65535,140],[u'Remarque',3,200,80]]
        form=MyForm('Model de relance',data,self)
        form.SetModel(model,{0:1,1:2,2:3})
        if form.exec_():
            idModel=form.MyModel.lastid
            self.fields[2].setModel(MyComboModel(self.parent,'GetModelsRelance()'))
            self.fields[2].Setid(idModel)
            self.fields[2].hidePopup()
       
    
class FormModesRelance(MyForm):   
    def __init__(self,idClient,data,parent):
        MyForm.__init__(self,u'Modes de Relance',data,parent)
        self.parent=parent
        self.idClient=idClient
        self.InactivateEnter()
        self.fields[0].setModel(MyComboModel(self.parent,'GetAllModesRelance()'))
        #suppresion impossible juste isactif. le delete est effectué au save relance
        #TODO: surcharger Onselection verifie si N°,email, adresse renseignés
        #Pas d'édition des modes de relance car doivent être liés à une action: envoyer courrier, sms, email, message vocal, Relance téléphonique manuelle 

        