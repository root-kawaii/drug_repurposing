from html import entities
import os.path
import csv

from pkg_resources import compatible_platforms
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


class ConfigParser:


    def __init__(self,ID_COLUMN,col,entities):
        #Specify config file
        a_yaml_file = open("config.yaml")
        parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

        #read into data structures
        entities = parsed_yaml_file['entities']
        relations = parsed_yaml_file['relations']
        dataset_file = parsed_yaml_file['file']


        #select relation from YAML
        for w in range(len(relations)):
            col.append(relations[w][1])
        col.append(ID_COLUMN)

        #Could generalize Vocabulary
        paths = parsed_yaml_file['Vocabulary']
        Vocabularies = []
        if(paths):
            for i in range(len(paths)):
                Vocabularies.append(Vocabulary(paths[0]))
