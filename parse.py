from html import entities
import os.path
import csv

from nlp import parse_indication_disease
from sqlalchemy import null
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

def create_synonyms(name, synonyms) -> ([]):

    sinonimi = set([])
    # Name
    #if len(name) >= 0:
    #    name = name[0]
    #sinonimi.add(name.text.upper().strip()) if not (name.text is None or name.text == "") else 0

    # Synonyms
    for syn in synonyms:#[0].findall("synonym"):
        sinonimi.add(syn.upper().strip()) if not (syn is None or syn == "") else 0
    '''
    # Products
    if len(products) > 1:
        raise ValueError("More <products>: Expected one.")
    for product in products[0].findall("product"):
        product_name = product.findall("name")[0]
        if not (product_name.text is None or product_name.text == ""):
            sinonimi.add(product_name.text.upper().strip())
        else:
            continue
    '''
    return sinonimi


def parse(entitiess,triple_list,ID_COLUMN,col,Vocabularies,relations,tree,pendingList,thresholdTSV):
        #CONDITION
    for entity in entitiess:
        cont += 1
        if(entity[1].endswith('.csv')):
            #name = elements.findall(entity[0])
            col_syn = []
            col_syn.append(entity[2])
            #NEED TO SET THIS AS PARAMETER
            col_syn.append("Entry name")
            dh = pd.read_csv(entity[1])
            print(dh.columns)
            df = pd.read_csv(entity[1], usecols=col_syn)
            df = df.dropna()
            if(col_query.size != 0):
                col_iter = np.delete(col_syn,0)
            else:
                col_iter = col_query
            name = []
            sinonimi = []
            for row in range(len(df)):
                name.append(df.iloc[row]["Entry"]) 
                #NEED TO SET THIS AS PARAMETER
                sinonimi.append(df.iloc[row]["Entry name"])
                sinonimi2 = create_synonyms(name, sinonimi)#, products)
                #products = elements.findall("products")
                id = df.iloc[row]["Entry"]
                #HANDLE THE VOCABULARIES INDEX
                
                if('protein' in Vocabularies):
                    w = Vocabularies[entity[0]]
                    w.dict_id_to_name[id] = sinonimi2
                    #think so
                    w.dict_name_to_id[sinonimi2] = id
                else:
                    Vocabularies[entity[0]] = Vocabulary(None)
                    w = Vocabularies[entity[0]]
                    w.dict_id_to_name[id] = sinonimi2
                    #think so
                    w.dict_name_to_id[sinonimi2] = id
        ## XML SYN ##
        if(entity[1].endswith('.xml')):
            name = tree.getroot().findall(entity[0])
            for el in name:
                #set this as parameter
                id2 = el.find("ID") 
                synonyms = el.findall("synonyms")
                #products = elements.findall("products")
                sinonimiXML = create_synonyms(id2, synonyms)#, products)
                #HANDLE THE VOCABULARIES INDEX
                w = Vocabularies[entity[0]]
                if(sinonimiXML and id2):
                    w.dict_id_to_name[id2].append(sinonimiXML)
        ## TSV SYN ##
        if(entity[1].endswith('.tsv')):
            #name = elements.findall(entity[0])
            col_syn = []
            col_syn.append(entity[2])
            #NEED TO SET THIS AS PARAMETER
            ##col_syn.append("Entry name")
            dh = pd.read_csv(entity[1])
            print(dh.columns)
            df = pd.read_csv(entity[1], usecols=col_syn)
            df = df.dropna()
            if(col_query.size != 0):
                col_iter = np.delete(col_syn,0)
            else:
                col_iter = col_query
            name = []
            sinonimi = []
            for row in range(len(df)):
                name.append(df.iloc[row]["Entry"]) 
                #NEED TO SET THIS AS PARAMETER
                sinonimi.append(df.iloc[row]["Entry name"])
                sinonimi2 = create_synonyms(name, sinonimi)#, products)
                #products = elements.findall("products")
                id = df.iloc[row]["Entry"]
                #HANDLE THE VOCABULARIES INDEX
                if('disease' in Vocabularies):
                    w = Vocabularies[entity[0]]
                    w.dict_id_to_name[id] = sinonimi2
                    #think so
                    w.dict_name_to_id[sinonimi2] = id
                else:
                    Vocabularies[entity[0]] = Vocabulary(None)
                    w = Vocabularies[entity[0]]
                    w.dict_id_to_name[id] = sinonimi2
                    #think so
                    w.dict_name_to_id[sinonimi2] = id


    df = pd.read_csv(entity[1])
    col_query = np.intersect1d(df.columns,col)
    #read and remove NaN
    df = pd.read_csv(entity[1], usecols=col_query)
    df = df.dropna()
    #remove column entry for iteration over other columns
    if(col_query.size != 0):
        col_iter = np.delete(col_query,0)
    else:
        col_iter = col_query
    for i in range(len(df)):
        for j in col_iter:
            res = df.iloc[i][j]
            a = Triple(df[entity[2]].iloc[i],j,res)
            if(lookUpVocabulary):
                triple_list.append(a)
            else:
                pendingList[entity[2]].append(a)
                #add to pending
    ## XML ##
    tree = Tree.parse(entity[1])
    #NEED TO GENERALIZE THIS PART
    #ACCORDING TO CONFIG FILE
    elements = tree.getroot().findall(entity[0])
    #dict_syn = {}
    #list_inter = []

    for element in elements:
        #ids = element.findall('products')
        '''
        for i in ids:
                if i.attrib.get("primary") == "true":
                    i.text.upper().strip()
                else:
                    raise ValueError("Error...")
        '''
        #for i in ids:
        for j in range(len(relations)):
            if(entity[0] in relations[j][0]):
                rel = element.findall(relations[j][1])
                #print(len(rel))
                for bb in rel:
                    #print(bb)
                    a = Triple(element,relations[j][1],bb)
                    if(lookUpVocabulary):
                        triple_list.append(a)
                    else:
                        pendingList[entity[2]].append(a)
                        #add to pending
    ## TSV ##
    csv_table=pd.read_table(entity[1],sep='\t')
    csv_table.to_csv('validDisease.csv',index=False)
    df = pd.read_csv(entity[1])
    col_query = np.intersect1d(df.columns,col)
    chemical_vocabulary = Vocabularies['disease']
    for line in df:
            #print("\rChemical - Disease n. " + f"{count:,}", end='') if count % 100000 == 0 else 0
            count += 1
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')

            chemical_id = 'MESH:' + sp_line[1]
            if chemical_id not in chemical_vocabulary.D_CHEMICAL:
                continue

            drugbank_id = chemical_vocabulary.D_CHEMICAL[chemical_id][0]
            disease_id = sp_line[4]
            inference_score = sp_line[7]

            if inference_score == "":  # No inference --> direct evidence
                triple_list.append(Triple(drugbank_id, "TREAT", disease_id))
                continue
            else:
                inference_score = float(inference_score)
            # TODO Use Inference relation name Marker/Mechanism or Therapeutic or Both
            if inference_score >= thresholdTSV:
                triple_list.append(Triple(drugbank_id, "TREAT", disease_id))
    








