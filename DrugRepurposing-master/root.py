import argparse
import os.path as check
import csv

from rootTriple import Triple
from rootSupport import*
#from diseaseVocabularyMESHOMIM import DiseaseVocabularyMESHOMIM
#from geneVocabulary import GeneVocabulary
#from Triple import Triple
#from support_function import save_list_triple, check_dir
#from diseaseVocabularyNameCode import DiseaseVocabularyNameCode
#from drugBankVocabulary import DrugBankVocabularydef

tree = Tree.parse(drugbank_path)

reader = csv.DictReader(file, delimiter='\t')

dict = {}

for index, row in enumerate(reader):
    #print("\rProtein n. " + f"{index:,}", end='') if count % 1000 == 0 else 0
    #count += 1
    # Collecting
    dict2 = {}
    protein_id = row['Entry']
    dict[protein_id]=dict2
    gene_id = row['Gene names']
    dict2["Gene names"]=gene_id
    disease = row['Involvement in disease']
    interact_id = row['Interacts with']
    pharmaceutical_use = row['Pharmaceutical use'].strip()
    dict[protein_id]= dict2 #ecc....aggiungo tutto il resto
















drugs = tree.getroot().findall("drug")

for index, drug in enumerate(drugs):
    print("\rDrugBank n. " + f"{index:,}" + "/" + f"{num_drugs:,}", end='') if index % 1000 == 0 else 0

    # DrugBank-ID
    ids = drug.findall("drugbank-id")
    drug_id = parse_ids(ids)
    if drug_id is None:
        continue

    # Dictionary DrugBank-Id <--> Commercial Name / Synonyms
    if create_dictionary:
        name = drug.findall("name")
        synonyms = drug.findall("synonyms")
        products = drug.findall("products")
        sinonimi = create_synonyms(name, synonyms, products)
        dict_syn[drug_id] = list(sinonimi)
