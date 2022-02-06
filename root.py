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

def parse_protein_id(protein_id) -> str:
    """
    Parse protein id
    :param protein_id: protein id
    :return: protein id of UniProt
    """
    return protein_id.upper().strip()


def parse_gene_id(gene_id, gene_vocabulary):
    """
    UniProt tells us the  corresponding gene of a protein and its synonyms. We take only the first one that should be
    the principal name.
    :param gene_id: the gene_id field of UniProt
    :param gene_vocabulary: vocabulary of genes
    :return:
    """
    if not (gene_id == [] or gene_id == "" or gene_id is None):
        gene = gene_id.split(" ")[0].upper().strip()
        if gene in gene_vocabulary.D_GENSYMBOL:
            return gene_vocabulary.D_GENSYMBOL[gene]
        else:
            return gene
    else:
        return None


def parse_interactions(interact_id, protein_id): #-> []:
    """
    A list of gene interactions is given. If the list contains 'Itself', the current protein ID is substituted.
    :param interact_id: list of protein interactions.
    :param protein_id: current protein id
    :return: a parse list of interactions.
    """
    if not (interact_id == [] or interact_id == "" or interact_id is None):
        interact_id = interact_id.replace("Itself", protein_id)
        return interact_id.split("; ")
    else:
        return []


def parse_disease(disease, disease_vocabulary_mesh_omim, nlp, disease_vocabulary_name_code):# -> []:
    """
    In the 'Involvement in disease' field is given the Disease ID of OMIM, with whom the protein is involved.
    We look for the pattern [OMIM:XXYYZZ]. Otherwise NER?
    :param disease: Involvement in disease field
    :param disease_vocabulary_mesh_omim: Vocabulary for conversion MESH-OMIM
    :param nlp: spacy NLP parser
    :param disease_vocabulary_name_code: object of disease vocabulary name-code from OMIM and CTD
    :return: the OMIM disease involved
    """
    list_result_return = []
    if not (disease == [] or disease == "" or disease is None):
        try:
            omim = "O" + disease[disease.index("[") + 1:disease.index("]")]
        except ValueError:
            doc = nlp(disease)
            result_ner = list(doc.ents)
            for i in result_ner:
                possible_disease = str(i).upper().strip()
                if possible_disease in disease_vocabulary_name_code.diz:
                    code = disease_vocabulary_name_code.diz[possible_disease]
                    list_result_return.append(code)

            return list_result_return

        if omim in disease_vocabulary_mesh_omim.D_OMIM:
            vocabulary_list = list(disease_vocabulary_mesh_omim.D_OMIM[omim])
            if vocabulary_list:
                list_result_return.append(vocabulary_list[0])
            else:
                list_result_return.append(omim)

        else:
            list_result_return.append(omim)

    return list_result_return

'''
def parse_pharmaceutical_use(pharmaceutical_use, nlp, disease_vocabulary_name_code, chemicals_vocabulary):# -> []:
    list_result_return_pharmaceutical = []
    list_result_return_disease = []
    if pharmaceutical_use == "":
        return [], []
    else:
        doc = nlp(pharmaceutical_use)
        result_ner = list(doc.ents)
        for i in result_ner:
            entity = str(i).upper().strip()
            if entity in disease_vocabulary_name_code.diz:  # TODO decidere se cercare Malattia/farmaco o entrambi
                code = disease_vocabulary_name_code.diz[entity]
                list_result_return_disease.append(code)
            if entity in chemicals_vocabulary.dict_name_to_id:
                code = chemicals_vocabulary.dict_name_to_id[entity]
                list_result_return_pharmaceutical.append(code)

        return list_result_return_pharmaceutical, list_result_return_disease
'''


def process_uniprot(uniprot_path, ctd_disease_vocabulary_path, gene_vocabulary_path,
                    encoding_file, association_file, interaction_file,
                    omim_vocabulary_path, chemicals_vocabulary_path):
    encoding_list = []
    association_disease_list = []
    interaction_list = []
    #disease_vocabulary = DiseaseVocabularyMESHOMIM()
    #disease_vocabulary.create_vocabulary(ctd_disease_vocabulary_path)
    #gene_vocabulary = GeneVocabulary(gene_vocabulary_path)
    #disease_vocabulary_name_code = DiseaseVocabularyNameCode(ctd_disease_vocabulary_path, omim_vocabulary_path)
    #chemicals_vocabulary = DrugBankVocabulary(chemicals_vocabulary_path)
    spacy_model = "en_ner_bc5cdr_md"
    #nlp = spacy.load(spacy_model)

    print("Processing Uniprot")
    count = 0
    with open(uniprot_path) as file:
        reader = csv.DictReader(file, delimiter='\t')
        for index, row in enumerate(reader):
            print("\rProtein n. " + f"{index:,}", end='') if count % 1000 == 0 else 0
            count += 1
            # Collecting
            protein_id = row['Entry']
            gene_id = row['Gene names']
            disease = row['Involvement in disease']
            interact_id = row['Interacts with']
            #pharmaceutical_use = row['Pharmaceutical use'].strip()

            # Elaboration
            protein_id = parse_protein_id(protein_id)
            gene_id = parse_gene_id(gene_id, gene_vocabulary)
            disease = parse_disease(disease, disease_vocabulary, nlp, disease_vocabulary_name_code)
            interact_id = parse_interactions(interact_id, protein_id)
            #uses_pharmaceutical, rel_disease = parse_pharmaceutical_use(pharmaceutical_use, nlp,
                                                                        #disease_vocabulary_name_code,
                                                                        #chemicals_vocabulary)  # TODO Usarli?

            # Triple Creation
            if gene_id is not None:
                encoding_list.append(Triple(protein_id, "ISENCODED", gene_id))
            for protein in interact_id:
                interaction_list.append(Triple(protein_id, "INTERACTWITH", protein))
            for item in disease:# + rel_disease:
                association_disease_list.append(Triple(protein_id, "ISINVOLVED", item))
            #for item in uses_pharmaceutical:
                association_disease_list.append(Triple(protein_id, "USEDIN", item))

        print("\rProtein n. " + f"{count:,}")

    # Save Triple list to .csv
    save_list_triple(interaction_file, interaction_list, "")
    save_list_triple(association_file, association_disease_list, "")
    save_list_triple(encoding_file, encoding_list, "")

def main(args):
    uniprot_path = args["uniprot"]
    disease_vocabulary_path = args["diseasevocabularypath"]
    encoding_path = args["encodingpath"]
    interaction_path = args["interactionpath"]
    disease_path = args["diseasepath"]
    gene_vocabulary_path = args["genevocabularypath"]
    omim_vocabulary_path = args["omimpath"]
    chemicals_vocabulary = args["chemicalpath"]

    if uniprot_path and not check.isfile(uniprot_path):
        raise ValueError(uniprot_path + " is Not a valid path")

    if not check_dir(encoding_path):
        raise ValueError(encoding_path + " is Not a valid path")

    if not check_dir(interaction_path):
        raise ValueError(interaction_path + " is Not a valid path")

    if not check_dir(disease_path):
        raise ValueError(disease_path + " is Not a valid path")

    if not check.isfile(disease_vocabulary_path):
        raise ValueError(disease_vocabulary_path + " is Not a valid path")

    if not check.isfile(gene_vocabulary_path):
        raise ValueError(gene_vocabulary_path + " is Not a valid path")

    if not check.isfile(omim_vocabulary_path):
        raise ValueError(omim_vocabulary_path + " is Not a valid path")

    if not check.isfile(chemicals_vocabulary):
        raise ValueError(chemicals_vocabulary + " is Not a valid path")

    process_uniprot(uniprot_path, disease_vocabulary_path, gene_vocabulary_path,
                    encoding_path, disease_path, interaction_path,
                    omim_vocabulary_path, chemicals_vocabulary)

main()