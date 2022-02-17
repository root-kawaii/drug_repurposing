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
from dbVocabulary import DrugBankVocabulary


#Specify the column for the ID of the database
ID_COLUMN = "Entry"
#list of the triples for graphs
triple_list = []

#Specify config file
a_yaml_file = open("config.yaml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

#read into data structures
entities = []
entities = parsed_yaml_file['entities']
relations = parsed_yaml_file['relations']
dataset_file = parsed_yaml_file['file']
only_relations = []
for i in relations:
    only_relations.append(i[1])

#print(entities)
#print(relations)
#print(only_relations)

#create comfortable columns for iterations and searches
for files in dataset_file:
    col = only_relations
    col.append(ID_COLUMN)
    df = pd.read_csv(files)
    col_query = np.intersect1d(df.columns,col)

    #read and remove NaN
    df = pd.read_csv(files, usecols=col_query)
    df = df.dropna()

#remove column entry for iteration over other columns
if(col_query.size != 0):
    col_iter = np.delete(col_query,0)

#Actually find the relations and create Triples and store them
for i in range(len(df)):
    for j in col_iter:
        res = df.iloc[i][j]
        for w in res:
            a = Triple(df[ID_COLUMN].iloc[i],j,res)
            triple_list.append(a)
        

#print(triple_list)

DrugVocabulary = DrugBankVocabulary('drugbank vocabulary.csv')
print(DrugBankVocabulary.dict_id_to_name)



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