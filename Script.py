#!/usr/bin/env python
# coding: utf-8

#importation des bibliothéques
import json
import csv
import pandas as pd
import re
import spacy
from spacy.matcher import Matcher 
from spacy.lang.fr.examples import sentences 
from spacy import displacy 
import visualise_spacy_tree
from IPython.display import Image, display
import pytextrank
from collections import Counter
from string import punctuation
import warnings


#on va ignorer les warnings du code pour que ca ne gache pas l'affichage de notre script
warnings.filterwarnings('ignore')

#ici , c'est trés important de donner le path complet du fichier CSV
csvfile = input("Donner le path complet de votre dataframe (CSV File) : ")

#lecture du fichier csv
data = pd.read_csv (csvfile)

print("")
print("")

#affichage du notre dataframe initiale
print("affichage du notre dataframe initiale")
print("---------------------------------------------")
print(data)

print("")
print("")



#structure du dataframe
print("structure du dataframe")
print("---------------------------------------------")
data.shape

print("")
print("")

data.info()

print("")
print("")

#on va seulent s'intéresser aux champs climatisation , salle de bain , fonds & description
newdata=data[[ 'climatisation', 'fonds' , 'salle_de_bain' , 'description']]

print("nouveau dataframe")
print("---------------------------------------------")
print(newdata)

print("")
print("")

#transformation du type du champ description en String
newdata["description"]=newdata["description"].astype(str)


#fonction qui nous permet de diviser le champ description en des phrases
def sentences(text):
    text = re.split('[.?]', text)
    clean_sent = []
    for sent in text:
        clean_sent.append(sent)
    return clean_sent


newdata['sent'] = newdata['description'].apply(sentences)


print("dataframe avec le champ sentences")
print("---------------------------------------------")
print(newdata)

print("")
print("")


#fonction qui va détecter les phrases concernant le champ climatisation
index=0
for column in newdata["sent"]:
    for x in range(len(column)):
            sentence = column[x]
            words = sentence.split()
            for word in words:
                if (word=="climatisation" or word=="climatiseur" or word=="ventilation"):
                    newdata["climatisation"][index] = sentence
    index=index+1



#fonction qui va détecter les phrases concernant le champ fonds
index=0
for column in newdata["sent"]:
    for x in range(len(column)):
            sentence = column[x]
            words = sentence.split()
            for word in words:
                if (word=="parking"):
                    newdata["fonds"][index] = sentence
    index=index+1



#fonction qui va détecter les phrases concernant le champ salle de bain
index=0
for column in newdata["sent"]:
    for x in range(len(column)):
            sentence = column[x]
            words = sentence.split()
            for word in words:
                if (word=="bain"):
                    #print(sentence)
                    #print(index)
                    newdata["salle_de_bain"][index] = sentence
    index=index+1


#affichage de la version finale du dataframe
print("version finale du dataframe")
print("---------------------------------------------")
print(newdata)

newdata.to_csv('data_final.csv')
print("")
print("")
print("dataframe convertit en fichier CSV et enregistré")







