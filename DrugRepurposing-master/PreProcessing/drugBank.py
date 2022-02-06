import xml.etree.ElementTree as Tree
import spacy
import argparse
import os.path as check

from Triple import Triple
from support_function import save_list_triple, true_xor, check_dir
from drugBankVocabulary import DrugBankVocabulary
from diseaseVocabularyNameCode import DiseaseVocabularyNameCode


def extract_disease(indication, nlp) -> []:
    """
    Use spacy nlp to extract the nouns of diseases form the textual indication
    :param indication: the textual indication for a drug
    :param nlp: the spacy nlp object
    :return: a list of possible disease detected
    """
    doc = nlp(indication)
    return list(doc.ents)


def parse_ids(ids) -> str:
    """
    Given a list of ids, return only the one with the primary attribute = DrugBank ID
    :param ids: list of ids tag
    :return: the DrugBank ID of a drug
    """
    for i in ids:
        if i.attrib.get("primary") == "true":
            return i.text.upper().strip()
        else:
            raise ValueError("No primary DrugBank ID")


def create_synonyms(name, synonyms, products) -> ([]):
    """
    Given a DrugBank ID create a list of possible name for that drug. Pharmaceutical and commercial names.
    :param name: name of the drug
    :param synonyms: list of synonyms of the drug
    :param products: list of commercial product
    :return: list of synonyms of a drug
    """
    sinonimi = set([])

    # Name
    if len(name) >= 0:
        name = name[0]
    sinonimi.add(name.text.upper().strip()) if not (name.text is None or name.text == "") else 0

    # Synonyms
    for syn in synonyms[0].findall("synonym"):
        sinonimi.add(syn.text.upper().strip()) if not (syn.text is None or syn.text == "") else 0

    # Products
    if len(products) > 1:
        raise ValueError("More <products>: Expected one.")
    for product in products[0].findall("product"):
        product_name = product.findall("name")[0]
        if not (product_name.text is None or product_name.text == ""):
            sinonimi.add(product_name.text.upper().strip())
        else:
            continue

    return sinonimi


def parse_target(targets, drug_id, dictionary) -> []:
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
        protein_interaction = target.findall("polypeptide")

        if protein_interaction:
            id_target = target.findall("polypeptide")[0].attrib.get("id")
        else:
            name = target.findall("name")[0].text
            try:
                id_target = dictionary.dict_name_to_id[name]
            except KeyError:
                id_target = None
            if id_target is None:
                id_target = name.upper().strip()
        azioni = target.findall("actions")[0]
        for action in azioni.findall("action"):
            actions.add(action.text.upper().strip()) if not (action.text is None or action.text == "") else 0
        for item in actions:
            interactions.append(Triple(drug_id, item, id_target))

    return interactions


def parse_indication_disease(indication, drug_id, nlp, disease_vocabulary_name_code) -> []:
    """
    Extract disease for a textual indication of a drug.
    :param indication: text indication
    :param drug_id: current DrugBank ID
    :param nlp: spacy nlp object
    :param disease_vocabulary_name_code: object of disease vocabulary name-code from OMIM and CTD
    :return: A triple of possible treatments for the diseases using that drug
    """
    list_of_indication = []
    indication_text = indication[0].text
    if not (indication_text is None or indication_text is "" or type(indication_text) == "NoneType"):
        for i in extract_disease(indication_text, nlp):
            possible_disease = str(i).upper().strip()
            if possible_disease in disease_vocabulary_name_code.diz:
                list_of_indication.append(Triple(drug_id, "TREAT", disease_vocabulary_name_code.diz[possible_disease]))
    return list_of_indication


def transform_list(lista) -> str:
    my_string = '|'.join(lista)
    return my_string


def save_vocabulary(file_name, vocabulary):
    """
    Save vocabulary of drugs into .csv file. If the file is present, it will be overwritten.
    :param file_name: destination file.
    :param vocabulary: vocabulary of drug
    """
    with open(file_name, mode='w+') as file:
        file.write("DrugBank ID,Synonyms\n")
        for key in vocabulary:
            testo = str(key) + "," + transform_list(vocabulary[key])
            file.write(testo)
            file.write('\n')


def process_drugbank(drugbank_path, dictionary_file, interaction_file, indication_file,
                     create_dictionary, create_interaction, create_indication_disease,
                     omim_vocabulary_path, ctd_disease_vocabulary_path):
    dict_syn = {}
    list_inter = []
    list_indication = []
    nlp = None
    disease_vocabulary_name_code = None

    fun = {create_dictionary: "Vocabulary",
           create_interaction: "Interaction Target",
           create_indication_disease: "Indication Disease"}

    print("Processing DrugBank " + str(fun[True]))

    tree = Tree.parse(drugbank_path)

    if create_indication_disease:
        spacy_model = "en_ner_bc5cdr_md"  # TODO cerca se da NER è un disease o un chemical...Non ho trovato nulla
        try:
            nlp = spacy.load(spacy_model)
            disease_vocabulary_name_code = DiseaseVocabularyNameCode(ctd_disease_vocabulary_path, omim_vocabulary_path)
        except ModuleNotFoundError:
            raise ValueError("Impossible to load spacy " + spacy_model)

    drugbank_vocabulary = DrugBankVocabulary(dictionary_file) if create_interaction else 0

    drugs = tree.getroot().findall("drug")

    num_drugs = len(drugs)

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

        # Relation Drug <--> Drug/Protein/Etc.
        if create_interaction:
            targets = drug.findall("targets")
            interactions = parse_target(targets, drug_id, drugbank_vocabulary)
            list_inter += interactions

        # Pharmaceutical Indication Drug <--> Disease
        if create_indication_disease:
            indication = drug.findall("indication")
            indications = parse_indication_disease(indication, drug_id, nlp, disease_vocabulary_name_code)
            list_indication += indications

    print("\rDrugBank n. " + f"{num_drugs:,}" + "/" + f"{num_drugs:,}")

    # Save result
    save_list_triple(interaction_file, list_inter, "") if create_interaction else 0
    save_list_triple(indication_file, list_indication, "") if create_indication_disease else 0
    save_vocabulary(dictionary_file, dict_syn) if create_dictionary else 0


def main(args):
    drugbank_path = args["drugbank"]
    vocabulary_file = args["vocabularypath"]
    interaction_file = args["interactionpath"]
    indication_file = args["diseasepath"]
    create_vocabulary = bool(args["vocabulary"])
    create_interaction = bool(args["interaction"])
    create_indication_disease = bool(args["disease"])
    omim_vocabulary_path = args["omimpath"]
    ctd_disease_vocabulary_path = args["ctdpath"]

    if drugbank_path and not check.isfile(drugbank_path):
        raise ValueError(drugbank_path + " is Not a valid path")

    if not true_xor(create_vocabulary, create_interaction, create_indication_disease):
        raise ValueError("Select only one process")

    if create_vocabulary and (vocabulary_file is None or not check_dir(vocabulary_file)):
        raise ValueError("To create a Dictionary of Drugs is needed an output path")

    if create_interaction and \
            (vocabulary_file is None or not check.isfile(vocabulary_file) or not check_dir(interaction_file)):
        raise ValueError("To create interaction is needed an output path a valid dictionary path")

    if create_indication_disease and (indication_file is None
                                      or not check_dir(indication_file)
                                      or not check.isfile(omim_vocabulary_path)
                                      or not check.isfile(ctd_disease_vocabulary_path)):
        raise ValueError("To create a indications of Drug is needed an output path")

    process_drugbank(drugbank_path, vocabulary_file, interaction_file, indication_file,
                     create_vocabulary, create_interaction, create_indication_disease,
                     omim_vocabulary_path, ctd_disease_vocabulary_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="DrugBank Parser")
    parser.add_argument("-P", "--drugbank", required=True, help="DrugBank data file")
    parser.add_argument("-V", "--vocabularypath", required=False, help="Vocabulary input/output data file")
    parser.add_argument("-I", "--interactionpath", required=False, help="Drug-Target output data file")
    parser.add_argument("-D", "--diseasepath", required=False, help="Drug-Disease output data file")
    parser.add_argument("-O", "--omimpath", required=False, help="Omim vocabulary data file")
    parser.add_argument("-C", "--ctdpath", required=False, help="CTD vocabulary disease data file")
    parser.add_argument("-v", "--vocabulary", required=False, action='store_true', help="Create Vocabulary DrugBank")
    parser.add_argument("-i", "--interaction", required=False, action='store_true',  help="Create Drug-Target file")
    parser.add_argument("-d", "--disease", required=False, action='store_true', help="Create Drug-Disease file")

    main(vars(parser.parse_args()))
