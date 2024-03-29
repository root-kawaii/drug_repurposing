from html import entities
import os.path
import csv
from Triple import Triple
import pandas as pd
import yaml
import io
import numpy as np


import argparse
import os.path as check
from Triple import Triple
from Vocabulary import Vocabulary, lookUpVocabulary
from parse import parse




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
col = parsed_yaml_file['Relations']
Columns = {}
if(col):
    for i in range(len(col)):
        step = col[i]
        Columns[step[0]] = step[1] 
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
    pendingList[steppo[0]] = []
        

#print(drugBankVocabulary.dict_id_to_name)

## need to set threshold
parse(entitiess,triple_list,ID_COLUMN,Columns,Vocabularies,relations,pendingList,thresholdTSV=0)


##for i in pendingList.values:
##    if(lookUpVocabulary(i)):
##        triple_list.append(i)

print('...')

##print(Vocabularies['drug'].dict_id_to_name)


with open("transcript.tsv", mode='a') as file:
    for element in triple_list:
        for i in range(len(col)):
            step = col[i]
            checkk = step[1]
            if(checkk == element.relation):
                file.write(element.relation)
                file.write(element.head)
                file.write(element.tail)
                file.write('\n')