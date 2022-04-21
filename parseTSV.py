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


def parseTSV(entity,triple_list,col,Vocabularies,threshold):
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
            if inference_score >= threshold:
                triple_list.append(Triple(drugbank_id, "TREAT", disease_id))


