from html import entities
import os.path
import csv
from Triple import Triple
import pandas as pd
import yaml
import io
import numpy as np
import xml.etree.ElementTree as Tree

import argparse
import os.path as check
from Triple import Triple
from Vocabulary import Vocabulary, lookUpVocabulary
from parseCSV import parseCSV
from parseXML import parseXML
#from disease import parseTSV
from parseTSV import parseTSV




#Specify the column for the ID of the database
ID_COLUMN = "Entry"
#SetUp
triple_list = []
entities = []
colP = []
colD = []
#Specify config file
a_yaml_file = open("config.yaml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

#read into data structures
entitiess = parsed_yaml_file['entities']
relations = parsed_yaml_file['relations']
dataset_file = parsed_yaml_file['file']

#NEED TO ADDRESS DIFFERENT ENTITIES SUCH AS DRUGS AND PROTEINS
#select relation from YAML
for w in range(len(relations)):
    if(relations[w][0]=='protein'):
        colD.append(relations[w][1])
    if(relations[w][0]=='protein'):
        colP.append(relations[w][1])
colP.append(ID_COLUMN)
#colD.append(ID_COLUMN)

#Could generalize Vocabulary
#This can be streamlined but right now reads into config file and creats a dicitonary of vocabularies
#Entity is the key and the vocabulary is the value
paths = parsed_yaml_file['Vocabulary']
Vocabularies = {}
if(paths):
    for i in range(len(paths)):
        step = paths[i]
        checkz = Vocabulary(step[0],step[2])
        Vocabularies[step[1]] = checkz

#we create a pending dictionary for the Triples whose tails are missing IDs
#sorted by the type of entity
#At the end of the program we look again in every dictionary looking for the ID and if successful we add triple
pendingList = {}
for w in range(len(entitiess)):
    steppo = entitiess[w]
    listo = []
    pendingList[steppo(0)] = listo
        

#print(drugBankVocabulary.dict_id_to_name)
cont = 0
for entity in entitiess:
    cont += 1
    if(entity[1].endswith('.csv')):
        parseCSV(entity,triple_list,ID_COLUMN,colP,Vocabularies)
    if(entity[1].endswith('.xml')):
        parseXML(entity,relations,triple_list,Vocabularies)  
    if(entity[1].endswith('.tsv')):
        csv_table=pd.read_table(entity[1],sep='\t')
        csv_table.to_csv('valid'+ cont + '.csv',index=False)
        dfT = pd.read_csv(entity[1])
        parseTSV(entity,relations,triple_list,colD,Vocabularies,cont)  
log = open("transcript.txt",'a')
for elemo in triple_list:
    log.write(elemo.__str__())


    '''
    
        if (create_interaction):
                    targets = drug.findall("targets")
                    interactions = parse_target(targets, ids, drugVocabulary)
                    list_inter += interactions
        
        # Pharmaceutical Indication Drug <--> Disease
        if (create_indication_disease):
            indication = drug.findall("indication")
            #disease_vocabulary_name_code = DiseaseVocabularyNameCode(ctd_disease_vocabulary_path, omim_vocabulary_path)
            #indications = parse_indication_disease(indication, ids, nlp, disease_vocabulary_name_code)
            list_indication += indications
        

    save_list_triple(interaction_file, list_inter, "") if create_interaction else 0
    save_list_triple(indication_file, list_indication, "") if create_indication_disease else 0
    save_vocabulary(dictionary_file, dict_syn) if create_dictionary else 0
    '''

for i in pendingList.values:
    if(lookUpVocabulary(i)):
        triple_list.append(i)

print('...')




'''
tsv_file = open("swissprot.tsv")
csv_table=pd.read_table(tsv_file,sep='\t')
csv_table.to_csv('swissprot.csv',index=False)
df = pd.read_csv("swissprot.csv")
sorted_df = df.sort_values(by=["Entry"], ascending=True)
print(sorted_df)

#read param
col = ["Length","Interacts with"]
df = pd.read_csv("swissprot.csv", usecols=col)
print(df)

df1 = df.where(df['Length'] != 140)
#print(df1)
df2 = df1.where(df1['Length'] < 400)

#print(df2)

df3 = df.query('Length < 400')

#print(df3)



#save it 
sorted_df.to_csv('sorted_swissprot.csv', index=False)

'''