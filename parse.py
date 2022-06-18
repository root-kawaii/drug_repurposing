from html import entities
import os.path
import csv
from re import L

from nlp import parse_indication_disease
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
import xml.etree.ElementTree as ET


from simplified_scrapy import SimplifiedDoc

doc = SimplifiedDoc()
doc.loadFile('DrugBank.xml', lineByline=True)




def create_synonyms(name, synonyms) -> ([]):

    sinonimi = set([])
    # Name
    #if len(name) >= 0:
    #    name = name[0]
    #sinonimi.add(name.text.upper().strip()) if not (name.text is None or name.text == "") else 0

    # Synonyms
    for syn in synonyms:#[0].findall("synonym"):
        sinonimi.add(syn) if not (syn is None or syn == "") else 0
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



def parse_target(targets, drug_id, dictionary,relations) -> []:
    """
    Identify targets of a drug. If no action is present for a target. The interaction is not saved.
    :param targets: list of <target>
    :param drug_id: current DrugBankID
    :param dictionary: dictionary to resolve association name <-> DrugBankID
    :return: Triple of interaction Drug -> Protein/DrugBank ID/etc.
    """
    interactions = []
    if len(targets) > 1:
        raise ValueError("More <targets>: Expected one.")

    for target in targets[0]:
        actions = set([])
        inter = target.findall(relations[3])
        for i in range(4,len(relations)-1):
            inter = inter.findall(relations[i])
            '''
        azioni = target.findall("actions")[0]
        for action in azioni.findall("action"):
            actions.add(action.text.upper().strip()) if not (action.text is None or action.text == "") else 0
        for item in actions:
            '''
        interactions.append(Triple(drug_id, relations[len(relations)], inter))

    return interactions


def parse(entitiess,triple_list,ID_COLUMN,col,Vocabularies,relations,pendingList,thresholdTSV):
        #CONDITION
    for entity in entitiess:    
        if(entity[1].endswith('.csv')):
            #continue
            #name = elements.findall(entity[0])
            col_syn = []
            col_syn.append(entity[2])
            #NEED TO SET THIS AS PARAMETER
            #col_syn.append("Entry name")
            df = pd.read_csv(entity[1], usecols=col_syn)
            #check if DROPNA drops NA rows or rows with missing features (axis=1 drops columns with NA)
            df = df.dropna(axis=1)
            if(len(col_syn) != 0):
                col_iter = np.delete(col_syn,0)
            else:
                col_iter = col_syn
            name = []
            sinonimi = []
            for row in range(len(df)):
                name.append(df.iloc[row][entity[2]]) 
                #NEED TO SET THIS AS PARAMETER
                sinonimi.append(df.iloc[row][entity[3]])
                sinonimi2 = create_synonyms(name, sinonimi)#, products)
                #products = elements.findall("products")
                id = df.iloc[row][entity[2]]
                #HANDLE THE VOCABULARIES INDEX
                
                if(entity[0] in Vocabularies):
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
            tree = ET.parse(entity[1])
            name = tree.getroot().findall(entity[0])
            for el in name:
                #set this as parameter
                id2 = el.find(entity[2])
                id2 = id2.text.upper().strip()
                print(id2)
                synonyms = el.findall(entity[3])
                #products = elements.findall("products")
                sinonimiXML = create_synonyms(id2, synonyms)#, products)
                #HANDLE THE VOCABULARIES INDEX
                w = Vocabularies[entity[0]]
                if(sinonimiXML!=None and id2!=None):
                    w.dict_id_to_name[id2].append(sinonimiXML)
        ## TSV SYN ##
        if(entity[1].endswith('.tsv')):
            #continue
            #csv_table=pd.read_table(entity[1],sep='\t')
            #csv_table.to_csv('validDisease.csv',index=False)
            ##df = pd.read_csv('validDisease.csv')
            #name = elements.findall(entity[0])
            col_syn = []
            col_syn.append(entity[2])
            #NEED TO SET THIS AS PARAMETER
            ##col_syn.append("Entry name")
            df = pd.read_csv(entity[1],sep='\t',usecols=col_syn)
            ##print(df.columns)
            name = []
            sinonimi = []
            print(len(df))
            for row in range(len(df)):
                name.append(df.iloc[row]) 
                #NEED TO SET THIS AS PARAMETER
                sinonimi.append(df.iloc[row][entity[3]])
                sinonimi2 = create_synonyms(name, sinonimi)#, products)
                #products = elements.findall("products")
                id = df.iloc[row][entity[2]]
                #HANDLE THE VOCABULARIES INDEX
                if(entity[0] in Vocabularies):
                    w = Vocabularies[entity[0]]
                    w.dict_id_to_name[id] = sinonimi2
                    #think so
                    for i in sinonimi2:
                        w.dict_name_to_id[i] = id
                else:
                    Vocabularies[entity[0]] = Vocabulary(None,None)
                    w = Vocabularies[entity[0]]
                    w.dict_id_to_name[id] = sinonimi2
                    #think so
                    for i in sinonimi2:
                        w.dict_name_to_id[i] = id

    for entity in entitiess:
        #print(entity[1])
        if(entity[1].endswith('.csv')):
            #continue
            df = pd.read_csv(entity[1])
            col_query = np.intersect1d(df.columns,col)
            #read and remove NaN
            df = pd.read_csv(entity[1], usecols=col_query)
            #CHECK
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
                    if(lookUpVocabulary(bb,Vocabularies,entity[0],pendingList)):
                        triple_list.append(a)
                    else:
                        pendingList[entity[2]].append(a)
                        #add to pending
        ## XML ##
        if(entity[1].endswith('.xml')):        
            ##tree = ET.parse(entity[1])
            #doc = SimplifiedDoc()
            #doc.loadFile('DrugBank.xml', lineByline=True)
            #NEED TO GENERALIZE THIS PART
            #ACCORDING TO CONFIG FILE
            elements = tree.getroot().findall(entity[0])
            for element in elements:
            ##print(elements[0])
            #dict_syn = {}
            #list_inter = []
                #indication = element.findall("indication")
                #drugID = element.find(entity[2])
                drugID = element.find(entity[2])
                drugID = drugID.text.upper().strip()
                print(drugID)
                indication = element.findall("indication")
                indications = parse_indication_disease(indication, drugID, None, Vocabularies)
                #print(indications)
                triple_list.append(indications)
                
                #if(indication):
                ##    indications = parse_indication_disease(indication, drugID,Vocabularies['disease'])
                ##    list_indication += indications
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
                        rel = parse_target(rel,drugID,Vocabularies[entity[0]],relations[j])
                        for bb in rel:
                            #print(bb)
                            ##a = Triple(drugID,relations[j][1],bb)
                            if(lookUpVocabulary(bb,Vocabularies,entity[0],pendingList)):
                                triple_list.append(bb)
                            else:
                                pendingList[entity[0]].append(bb)
                                #add to pending
        ## TSV ##
        if(entity[1].endswith('.tsv')):
            col_syn = []
            col_syn.append(entity[2])
            #NEED TO SET THIS AS PARAMETER
            ##col_syn.append("Entry name")
            df = pd.read_csv(entity[1],sep='\t',usecols=col_syn)
            df = df.dropna(axis=1)
            #remove column entry for iteration over other columns
            if(col_query.size != 0):
                col_iter = np.delete(col_query,0)
            else:
                col_iter = col_query
            for i in range(len(df)):
                for j in col_iter:
                    res = df.iloc[i][j]
                    a = Triple(df[entity[2]].iloc[i],j,res)
                    if(lookUpVocabulary(bb,Vocabularies,entity[0],pendingList)):
                        triple_list.append(a)
                    else:
                        pendingList[entity[2]].append(a)
                        #add to pending











