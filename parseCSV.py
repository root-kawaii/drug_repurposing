from html import entities
import os.path
import csv

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
from Vocabulary import Vocabulary

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


def parseCSV(entity,triple_list,ID_COLUMN,col,Vocabularies):
        #CONDITION
    if (1):
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
            sinonimi.append(df.iloc[row]["Entry name"])
            sinonimi2 = create_synonyms(name, sinonimi)#, products)
            #products = elements.findall("products")
            id = df.iloc[row]["Entry"]
            #HANDLE THE VOCABULARIES INDEX
            
            if('protein' in Vocabularies):
                w = Vocabularies[entity[0]]
                w.dict_id_to_name[id] = sinonimi2
            else:
                Vocabularies[entity[0]] = Vocabulary(None)
                w = Vocabularies[entity[0]]
                w.dict_id_to_name[id] = sinonimi2
    syn = {}
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
            a = Triple(df[ID_COLUMN].iloc[i],j,res)
            triple_list.append(a)





    return syn