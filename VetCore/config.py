# -*- coding: utf8 -*-

import os


DEBUG=True
DEBUG_AFFICHE_MESSAGE_CONSOLE=True  #TODO: a enlever lorsuqe les msg d erreurs seront geres par gestion_erreurs.py
#DEBUG = True



#user='root'#pour ouvrir la base
Path_Analyses='../Archives/Analyses/'
Path_Icons='../images/'

repertoire='/home/francois/Programmes/Kiwi/OpenVet/OpenVet/'
WorkingPath='/media/Datas/Kiwi/OpenVet'
dbCodec='ISO-8859-1'
#dbCodec='UTF-8'
user='root'
password='horizons'

if os.path.exists('/home/yvon') :
    repertoire='/home/yvon//Documents/programmation/openvet2/openvet2_python/'
    user='user_openvet'
    password='0000'


#**************************************defferentes version a tester**************
#database='OpenVet10b'
#database='OpenVet10c'   
#database='OpenVet10d'  #table rue sans idAdresse (=>plusieurs adresses peuvent avoir la mm rue / adresseHistorique = simple lien idclient, idadresse
database='OpenVet12'

host='localhost'
VilleCompletes=True #remplit la base avec toutes les villes de france




nomdatabase=database
#nomdatabasedebug= 'openvetdebug'
#if debug :
#    nomdatabase=nomdatabasedebug
    
passe_confirmation="123"    #password pour confirmer les operations critiques/dangereuses (ex effacer un client)
TAILLEDEBUTVILLE=4          #affiche les villes dans la liste a partir de 4 caracteres
TAILLETELEPHONE=10

IDUSER=1  # ************  chaque utilisateur openvet a un id different
