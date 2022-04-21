
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
from Vocabulary import Vocabulary


def create_synonyms(name, synonyms) -> ([]):

    sinonimi = set([])
    # Name
    #if len(name) >= 0:
    #    name = name[0]
    #sinonimi.add(name.text.upper().strip()) if not (name.text is None or name.text == "") else 0

    # Synonyms
    for syn in synonyms:#[0].findall("synonym"):
        sinonimi.add(syn.text.upper().strip()) if not (syn.text is None or syn.text == "") else 0
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


def parseXML(entity,relations,triple_list,Vocabularies):
    if (1):
        name = elements#.findall(entity[0])
        for el in name:
            id2 = el.find("ID") 
            synonyms = el.findall("synonyms")
            #products = elements.findall("products")
            sinonimi = create_synonyms(id2, synonyms)#, products)
            #HANDLE THE VOCABULARIES INDEX
            w = Vocabularies[entity[0]]
            if(sinonimi and id2):
                w.dict_id_to_name[id2].append(sinonimi)
    #print('yyy')
    syn = {}
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
                    a = Triple(element,'INTERACTS WITH',bb)
                    triple_list.append(a)
                    print(a.__str__())
        
    #CONDITION


    return syn