# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re
import os
import codecs
import time
from decimal import Decimal
from MyGenerics import *
from PyQt4 import QtCore, QtGui, QtSql


path = '/media/Datas/Kiwi/OpenVet0.2'
path = '../'
pathimport = path + 'Imports/'
erreur = False


def FormatName(chaine,codec='utf8'):    #TODO: maxlength for truncate
    chaine=chaine.decode(codec)
    out=[]
    for i in chaine.split(' '):
        if i=="DE":
            out.append('de')
        elif i[:2]=="D\'":
            out.append('d\''+i[2]+i[3:].lower())
        else:
            if len(i)>1:
                out.append(i[0]+i[1:].lower())
            else:
                out.append(i)
    chaine=' '.join(out)
    return chaine


def ExtractNumeric(chaine):
    r = re.findall(r'[0-9]*[ ,]?[0-9]+', chaine)
    if len(r) > 0:
        r[0] = r[0].strip()
    else:
        erreur = True
        r = ['Nombre non trouvé']
    return r

def ExtractUnit(chaine, nombre):
    unites = ['g', 'mg', 'UI', 'CH']
    pattern = re.compile('|'.join(unites))
    start = chaine.find(nombre)
    if start == -1:
        erreur = True
        r = ['Nombre invalide pour unité.']
        return r
    r = re.findall(pattern, chaine[start + len(nombre):])
    if len(r) == 0:
        erreur = True
        r = ['Unité inconnue.']
    return r[0]

def ExtractForme(chaine, isquantitatif):
    formes = ['comprimé', 'goutte', 'poudre', 'ml']
    pattern = ''
    chform = '|'.join(formes)
    if isquantitatif:
        pattern = '[Ss]oit '
        pattern = pattern + '([0-9]*[ ,]?[0-9]+.+)(' + chform + ')([^\.]+)'
    else:
        pattern = '(.+ )(' + chform + ')([^\.]+)'
        # éliminer phrase avant . si il y en a?
    pattern = re.compile(pattern)
    r = re.findall(pattern, chaine)
    if len(r) == 0:
        erreur = True
        r = ['Forme inconnue']
    return ''.join(r[0])

def GetListProp(name):
    fin = open(name, 'r')
    index = 0
    lignes = ''
    liste = []
    valid = False
    for i in fin:
        if not re.match(r'^[1-9]\.', i) is None:
            index += 1
            if valid:
                liste.append(lignes.strip())
            lignes = ''
            valid = False
        else:
            if index in [1, 2, 3, 5, 7, 13, 27]:
                valid = True
                if index in [2, 27]:
                    lignes = lignes + i
                else:
                    if len(i) > 1:
                        lignes = lignes + ' ' + i.strip()        
    fin.close()
    return liste

def GetSubstances(chaine):
# extraction substances actives
    comp = chaine
    start = comp.find('Substance(s) active(s)') + 26
    if start == 25:
        start = 0
    end = comp.find('\n\n', start)
    comp = comp[start:end]
    comp = [i for i in comp.split('\n')]
    substances = []
    for i in comp:
        r = re.findall(r' \.* +[0-9]', i)
        if len(r) == 0:
            continue
        end = i.index(r[0])
        med = i[:end].strip()
        qte = ExtractNumeric(i)[0]
        unit = ExtractUnit(i, qte)
        substances.append([med.lower(), qte, unit])
    return substances

def GetPosologie(chaine, substances):
    # extraction posologie
    comp = chaine
    quantitatif = True
    start = 0
    doses = []
    for i in substances:
        r = re.findall('[0-9]*[ ,]?[0-9]+.+de ' + i[0] + ' par ', comp[start:])
        if len(r) > 0:
            qte = ExtractNumeric(r[0])[0]
            unit = ExtractUnit(r[0], qte)
            doses.append([i[0], qte, unit])
            start = comp[start:].index(r[0]) + len(r[0])
    if len(doses) == 0:
        quantitatif = False
    else:
        quantitatif = True
    forme = ExtractForme(comp, quantitatif)
    return[doses, forme]

def GetPresentation(chaine):
    # extraction présentations
    comp = chaine
    comp = [i for i in comp.split('\n')]
    presentations = []
    amm = False
    for i in comp:
        r = re.findall(r'FR/.+[0-9]+ [0-9]{1,2}/[12][0-9]{3}', i)
        if len(r) == 1:
            amm = True
            continue
        else:
            if amm:
                presentations.append(i.replace('.', ' ').split())
            else:
                r1 = re.findall(r'[^:]+', i)
                presentations.append(r1[0].replace('.', ' ').strip())
    return presentations

def GetDecimal(chaine,Newchaine=False):
        chaine=chaine.replace('\'', '')
#        sols=re.findall(r'[0-9]+[ ,]?[0-9]*',chaine)
        chaine=re.sub(r'[uU]ne?','1',chaine)
        sols = re.findall(r'[0-9 ,]+', chaine)
        try:
            numb= Decimal([i for i in sols if len(i.strip()) > 0][0].replace(',', '.').replace(' ', ''))
        except:
            numb= Decimal('0')
        if Newchaine:
            return(numb,chaine.replace(',','.'))
        else:
            return numb

def ExtractUnite(chaine):
    return re.sub(r'[0-9, ]|une?','',chaine)
    

def Getunite(chaine):
        sols = re.findall(r'([0-9 ,]+)(DL50|kBq|mEq|millions UI|million.*internationales|[a-z]+)', chaine)
        sol = [i for i in sols if i[0] != ' ']
        if len(sol) == 0:
            return 'aucune'
#         elif sol[0][1]=='milliard':
#             print
        else:
            if sol[0][1] in ['bar', 'x', 'bact', 'ampoule', 'dose', 'milliards']:
                return 'aucune'
            else:
                return sol[0][1]

def GetShortPresentation(chaine):
    first = re.findall(r'(^[0-9 ]*\S+)', chaine)  # TOTEST r'(^[0-9 ]*\S[^\(\)]+)(?:\(s\))?[ -]'
    last = re.findall(r'de ([0-9, ]+\S+$)', chaine)
    if len(first) == 0:
        print 'erreur avec %s' % chaine    
    if len(last) == 0:
        last = re.findall(r'de ([0-9, ]+\S[^\( ]+)', chaine)
        if len(last) == 0:
            last = ['']       
    return ' '.join([first[0].replace('(s)', ''), last[0].replace('(s)', '')])  

def GetVoieAdministration(chaine):
    sel = re.findall(ur'ophtalmique|auriculaire|gingivale|buccale|dentaire|[^-]?cutanée|intradermique|transdermique|nasale|inhalée|rectale|vaginale|orale|sublinguale|sous-cutanée|intraveineuse|intramusculaire|intrapéritonéale|intra-articulaire|périarticulaire|péridurale|périneurale|intralésionnelle|infiltration', chaine.decode('latin-1'))  
    if len(sel) == 0:
        sel = ['autre']
    return ','.join(sel) 
            
def FormatSelection(liste):
    return[liste[0], liste[5],liste[1], liste[2], liste[3], max('1' * liste[4], '0')]


def ImportComposition(filin='LCompSpeHum.txt', filout='CompHum.txt'):
    print 'Compositions'
    finlog = codecs.open(pathimport + filin, 'r', encoding='iso-8859-1')
    molecules = []
    refs = []
    for line in finlog:
        words = line.split('\t')
        if len(words) > 5:
            if words[0] not in refs:
                refs.append(words[0])
#             if words[0]=='60092590':
#                 print words
            longname=re.sub(r' POUR PR.PARATIONS HOM.OPATHIQUES| BASE| ANHYDRE| SODIQUE','',words[3])
            shortname = re.sub(r'(^\S+ATE D[E\'] ?)|( \(.+\))|(,.+$)|( \S*HYDRAT\S+$)', '', longname) 
            if longname.count(':'):
                longname=longname[longname.index(':')+1:].strip()
            if shortname.count(':'):
                shortname=shortname[shortname.index(':')+1:].strip()
            if words[3].count('HOMÉOPATHIQUES'):
                medoc = [0, words[0], words[1], longname, '0,0', words[5], True,shortname]
            else:
                medoc = [0, words[0], words[1], longname, words[4], words[5], False,shortname]
            molecules.append(medoc)
    finlog.close()
    selref = []
    exclude = ['DE', 'SULFATE']     #pourquoi c'est faire déjà dans doublon?
    for ref in refs:
        selection = [[i[1], i[3], i[4], i[5], i[6],i[7]] for i in molecules if i[1] == ref and i[4] != '']
        while len(selection) > 1:
            doublon = [index for index, i in enumerate(selection[1:]) if len([j for j in i[1] if j in selection[0][1] and j not in exclude]) > 0]
            if len(doublon):
                index = doublon[0] + 1
                if GetDecimal(selection[0][2]) > GetDecimal(selection[index][2]):
                    selref.append(FormatSelection(selection[index]))
                else:
                    selref.append(FormatSelection(selection[0]))
                selection.pop(0)
                selection.pop(0)
            else:
                selref.append(FormatSelection(selection[0]))
                selection.pop(0)
        if len(selection) == 1:
            selref.append(FormatSelection(selection[0]))       
    foutlog = codecs.open(pathimport + filout, 'w', encoding='utf-8')
    uq = []
    for i in selref:
        if i not in uq:  # remove doublons
            uq.append(i)
            foutlog.write(';'.join(i) + '\n')
    foutlog.close() 
    
def ImportSpecialite(filin='LSpeHum.txt', filout='SpeHum.txt'):
    print "Specialite"
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='iso-8859-1')
    for line in finlog:
        line = line.replace(';', ',')
        words = line.split('\t')
        if len(words) > 5:
            words[1] = words[1].replace('\"', '')
            names = words[1].split()
            if len(names[0]) < 6 or 'Enreg homéo' in words[5]:
                name = ' '.join([names[0], names[1]])
            else:
                name = names[0].strip('.,')
            if 'Enreg homéo' in words[5]:
                selection.append([words[0], name, words[1].split(',')[0], ' ', ' ', '1'])
            else:
                Vadmin = GetVoieAdministration(words[3]).encode('latin-1')
                selection.append([words[0], name, words[1].split(',')[0], words[2], Vadmin, '0'])
    finlog.close()   
    foutlog = codecs.open(pathimport + filout, 'w', encoding='utf-8')
    for i in selection:
        foutlog.write(';'.join(i) + '\n')
    foutlog.close() 
    
def ImportPresentation(filin='LPresSpeHum.txt', filout='PresHum.txt'):
    print "Présentation"
    selection = []
    finlog = codecs.open(pathimport + 'LPresSpeHum.txt', 'r', encoding='iso-8859-1')
    for line in finlog:
        words = line.split('\t')
        if len(words) > 5:
            short = GetShortPresentation(words[2])
            selection.append([words[0], short])
    finlog.close()   
    foutlog = codecs.open(pathimport + 'PresHum.txt', 'w', encoding='utf-8')
    for i in selection:
        foutlog.write(';'.join(i) + '\n')
    foutlog.close() 


def ImportClasseTherapeutique(filin,filout,parent):
    selection=[]
    header=None
    finlog = codecs.open(pathimport + filin, 'rU', encoding='utf-8')
    iterator=iter(finlog)
    line=iterator.next()
    while not 'INDEX . . .' in line:
        line=re.sub(u'\. +','. ',line)
        sol=re.findall(ur'(([0-9]{1,2}\.)+)',line)
        if len(sol)>0:
            if sol[0][0]=='2.3.':
                print line
        sols=re.findall(ur'(([0-9]{1,2}\.)+ [^\.]+)',line)
        if len(sols)>0:
            newline=sols[0][0]
            if sols[0][0][-1:]=='\n':
                line=line+iterator.next()
                sols=re.findall(ur'(([0-9]{1,2}\.)+ [^\.]+)',line)
                newline=re.sub(r'\n *',' ',sols[0][0])
            selection.append(newline)
            header=re.findall(ur'(([0-9]{1,2}\.)+)',line)[0][0]
            index=1
        else:
            sols=re.findall(ur'\S[^\.]+ . . .',line)
            if len(sols)>0:
                if len(re.findall(r'[a-z]+',sols[0]))>0 and not header is None:
                    selection.append(header+'%i. '%index+sols[0][:-6])
                    index+=1
                    print sols
        line=iterator.next()
    finlog.close()
    foutlog = codecs.open(pathimport + filout, 'w', encoding='utf-8')
    for i in selection:
        foutlog.write(i+'\n')
    foutlog.close() 


def GetListeAdministration(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
#         if len(words[4].split(','))>1:
#             print words[4].split(',')
        for word in words[4].split(','):
            if word.strip() not in selection and len(word.strip()) > 0:
                selection.append(word.strip())
    finlog.close()
    return selection

def HomogenMolecule(chaine,codec='latin-1'):
    chaine=re.sub(r' \S+HYDRATÉE?','',chaine.decode(codec))
    tmp=re.findall(r'\(\S+ D[\'E]\)',chaine)
    if len(tmp)>0:
        chaine=re.sub(r'\(\S+ D[\'E]\)','',chaine)
        esp=''
        if tmp[0][-2:-1]=='E':
            esp=' '
        chaine=tmp[0].replace('(','').replace(')','')+esp+chaine
    return chaine.encode(codec)
        
def GetListeMolecule(filin):
    selection = []
    myliste=[]
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        if isVaccin(words[2],words[4]):
            continue
        words[2]=HomogenMolecule(words[2],'utf8')
        if words[2].strip() not in selection and len(words[2].strip()) > 0:
            selection.append(words[2].strip())
            #TODO: GET famille therapeutique
            myliste.append([words[2].strip(),words[1].strip(),words[0]])
    finlog.close()
    return myliste

def GetUniteAdministration(chaine):
    nchaine = unicode(chaine.decode('latin-1'))
    if 'buvable' in chaine:
        return ('solution buvable', False)
    sols = re.findall(ur'(suspension|solution)(injectable|perfusion|reconstituée|acides aminés|prête)?', nchaine)
    if len(sols)>0:
        return ('solution injectable', True)
    sols = re.findall(ur'comprimé|gélule|capsule', nchaine,re.U)
    if len(sols) > 0:
        return (sols[0].encode('latin-1'), False) 
    else:
        return (chaine, False)
    
def GetListeUniteMedoc(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        word = words[3].strip()
        if words[5].strip() == '0':  # if isHomeo skip
            word = GetUniteAdministration(word)
            if word not in selection:
                selection.append(word)
    finlog.close()
    return selection

def GetListeContenant(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        word = words[3].strip()
        if word not in selection:
            selection.append(word)
    finlog.close()
    return selection

def GetListeUniteMolecule(filin):
    selection = []
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        words = line.split(';')
        word = words[3]
        valeur = GetDecimal(word)
        unite = Getunite(word)
        try:
            unite = unite.strip()
        except:
            print 'Erreur %s' % word
        if unite not in selection:
            selection.append(unite)
    finlog.close()
    return selection

def isVaccin(word1,word2,codec='latin-1'):
    sol1=re.findall(ur'VIRUS|ATTÉNUÉ|SOUCHE|NEISSERIA MENINGITIDIS|PNEUMOCOCCIQUE', word1.decode(codec))
    sol2=re.findall(ur'vaccin', word2.decode(codec))
    return len(sol1)>0 or len(sol2)>0

def GetComposition(word1,word2):
    valeur1,word1 = GetDecimal(word1,True)
    try:
        word1=word1[word1.index(str(valeur1))+len(str(valeur1)):]
    except:
        print 'erreur valeur pour %s'%word1
        valeur1=-1.0
    unite=re.findall(r'\S+',word1)
    if len(unite)==0:
        print 'erreur pour %s'%word1
        unite=''
    else:
        unite=unite[0]
    unite=unicode(unite.decode('latin-1'))
    unite=re.sub(r'[Mm]illigrammes?','mg',unite)
    unite=re.sub(r'[Mm]icrogrammes?','µg',unite)
    unite=re.sub(r'[Nn]anogrammes?','mg',unite)
    unite=re.sub(r'[Gg]rammes?','g',unite)
    unite=re.sub(r'[Ll]itres?','l',unite)
    unite=re.sub(r'[Mm]illilitres?','ml',unite)
    unite=re.sub(r'[Mm]icrolitres?','µl',unite)
    unite=re.sub(ur'[mM]illions? d\'unités? internationales?|millions UI','MUI',unite)
    unite1=unite
    valeur2,word2 = GetDecimal(word2,True)
    try:
        word2=word2[word2.index(str(valeur2))+len(str(valeur2)):]
    except:
        pass
    unite2=re.findall(r'\S+',word2)[0]
#    unite2=GetUniteAdministration( ExtractUnite(word2))
    return(valeur1, unite1,valeur2,unite2)

        
def SaveVoiesAdministration(filin, parent):
    model = MyModel('VoieAdministration', 0, parent)
    for i in GetListeAdministration(filin):
        model.SetNew([0,i, QVariant(), True])   #unicode(i.decode('latin-1'))
        model.New()
        model.Update()

def SaveClassesTherapeutique(filin,parent=None):
    model = MyModel('ClasseTherapeutique', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split('. ')
#         data = []
#         data.append(QVariant(i[0]),QVariant(i[1]))
        model.SetNew([0,QVariant(i[0]),QVariant(i[1]),'',1,''])
        model.New()
        model.Update()
    
def SaveMedicament(filin, parent=None):
    model = MyModel('Medicament', 0, parent)
    modelRef = MyModel('VoieAdministrationRef', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split(';')
        data = []
        for j in i:
            j = j.strip()  #.decode('latin-1')
            if len(j) == 0:
                j = QVariant()
            data.append(j)
        ishomeo = True
        isinj = False
        isvaccin=False
        if i[5].strip() == '0':
            ishomeo = False               
            isinj = GetUniteAdministration(i[3])[1]
            if 'VACCIN' in data[2]:
                isvaccin=True
        model.SetNew([0, FormatName(data[1]), data[2], 'H' + data[0], ishomeo, isinj,isvaccin, data[3], QVariant(), 0, 1, ''])
        model.New()
        idMedicament = model.Update()
        # Save Voies Administrations in VoieAdministrationRef
        if data[4] == QVariant():
            continue
        if idMedicament.toInt()[1]:
            idMedicament = idMedicament.toInt()[0]
            for i in data[4].split(','):
                idVoie = model.MyRequest.GetInt('CALL GetidVoieAdmin(\"%s\")' % i, 0)
                if not idVoie is None:
                    modelRef.SetNew([0,idVoie,idMedicament,1,''])
                else:
                    print u'%s non trouvé dans la base' % i
            modelRef.New()
            modelRef.Update()

def SavePresentation(filin, parent):
    model = MyModel('Presentation', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split(';')
        i[1] = i[1].strip()
        idMedicament = model.MyRequest.GetInt('CALL GetidMedicament_Cip(\"H%s\")' % i[0], 0)
        #Extract idUnite & NbUnite. NULL if not found
        unite=model.MyRequest.GetLine('CALL ExtractidUnite(\'%s\',\'Galen\')'%','.join(i[1].split()))
        try:
            idunite=unite[0].toInt()[0]
        except:
            idunite=QVariant()
        try:
            nbunite=i[1].split()[unite[2].toInt()[0]-1]
            nbunite=int(nbunite)
        except:
            nbunite=QVariant()
        if not idMedicament is None:
            model.SetNew([0, idMedicament, i[1], idunite, nbunite, True, ''])
            model.New()
            model.Update()
        else:
            print 'H%s non trouvé' % i[0]

def SaveMolecules(filin, parent):
    model = MyModel('Molecule', 0, parent)
    for i in GetListeMolecule(filin):
        if not model.MyRequest.GetInt('CALL isVaccin_Cip(\"H%s\")'%i[2],0):
            model.SetNew([0,FormatName(i[0]),FormatName(i[1]),QVariant(),QVariant(),True,False])
            model.New()
            if model.Update()==-1:
                print model.lasterror+' pour :'
                print i
                
def SaveCompositions(filin,parent):
    logs=[]
    medmodel=MyModel('Medicament', 0, parent)
    model = MyModel('MedicamentConcentration', 0, parent)
    finlog = codecs.open(pathimport + filin, 'r', encoding='utf-8')
    for line in finlog:
        i = line.split(';')
        i[2] = i[2].strip()
        i[4] = i[4].strip()
        idMedicament = model.MyRequest.GetInt('CALL GetidMedicament_Cip(\"H%s\")' % i[0], 0)
        if idMedicament is None:
            logs.append('H%s non trouvé' % i[0])
            print 'H%s non trouvé' % i[0]
            continue
        medmodel.Setid(idMedicament)
        pi2=i[2]
        tmp=HomogenMolecule(i[2],'utf8')    #.decode('utf8')
        idMolecule = model.MyRequest.GetInt('CALL GetidMolecule(\"%s\")' % tmp, 0)
        if idMolecule is None:
            if isVaccin(i[2],i[4],'utf8'):
                medmodel.listdata[6]=QVariant(True)
                medmodel.Update()
            else:
                logs.append('%s non trouvé' % tmp)
                print '%s non trouvé' % tmp
            continue
        if i[5].strip()==u'0':
            compo=GetComposition(i[3],i[4])
            idUnite1=model.MyRequest.GetInt('CALL GetidUnite(\"%s\")'%compo[1],0)
            if idUnite1 is None:
                idUnite1=QVariant()
            idUnite2=model.MyRequest.GetInt('CALL GetidUnite(\"%s\")'%compo[3],0) 
            if idUnite2 is None:
                idUnite2=QVariant()
            model.SetNew([0,idMolecule,idMedicament,i[3][:60], float(compo[0]),idUnite1,i[4][:60],float(compo[2]),idUnite2,True,''])
        else: 
            model.SetNew([0,idMolecule,idMedicament,QVariant(),QVariant(),QVariant(),QVariant(),QVariant(),QVariant(),True,''])
        model.New()
        if model.Update()==-1:
            print ('erreur',i[2],i[0],i[3],i[4])   
    finlog.close()
    flog=open('importVidal.log','w')
    for i in logs:
        flog.write(i+'\n')
    flog.close()      
    
# ImportComposition()
# ImportSpecialite()
# ImportPresentation()
# ImportClasseTherapeutique('REPFR_2014.txt','VClasses.txt',window)


# for i,j in enumerate(GetListeAdministration('SpeHum.txt')):
#     print '%i.%s'%(i+1,j)
# for i,j in enumerate(GetListeUniteMedoc('SpeHum.txt')):
#     print '%i.%s'%(i+1,j)
# for i,j in enumerate(GetListeContenant('CompHum.txt')):
#     print '%i.%s'%(i+1,j)      
# for i,j in enumerate(GetListeUniteMolecule('CompHum.txt')):
#     print '%i.%s'%(i+1,j)

if __name__ == '__main__':
    t0=time.time()
    app = QtGui.QApplication(sys.argv)
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName ( config.host )
    db.setUserName ( config.user )
    db.setPassword ( config.password )
    db.setDatabaseName(config.database)
    if not db.open():
        QtGui.QMessageBox.warning(None, "Opencompta",
            QtCore.QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)  
    window = QDialog()
    window.show()
    SaveClassesTherapeutique('VClasses.txt',window)
#     SaveVoiesAdministration('SpeHum.txt',window)
#     SaveMedicament('SpeHum.txt',window)
#     SavePresentation('PresHum.txt',window)
#     SaveMolecules('CompHum.txt',window)
#     SaveCompositions('CompHum.txt',window)
    print time.time()-t0  
    sys.exit(app.exec_())   


#     extrait=[None]*len(liste)
#     extrait[0]=liste[0]
#     extrait[1]=GetSubstances(liste[1])
#     extrait[2]=re.sub(r'\.$','',liste[2])
#     extrait[3]=liste[3].replace('.','').replace(' et ',', ').lower().split(',')
#     extrait[4]=re.sub(r'\.$','',liste[4])
#     extrait[5]=GetPosologie(liste[5],extrait[1])
#     extrait[6]=GetPresentation(liste[6])


