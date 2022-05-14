# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy
import Triple

# Load English tokenizer, tagger, parser and NER


def extract_disease(text): # Process whole documents
    nlp = spacy.load("en_ner_bc5cdr_md")
    doc = nlp(text)
    # Analyze syntax

    #print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    #print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
    
    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)


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
        for i in extract_disease(indication_text):
            possible_disease = str(i).upper().strip()
            if(disease_vocabulary_name_code.dict_name_to_id[possible_disease] or disease_vocabulary_name_code.dict_id_to_name[possible_disease] ):
                list_of_indication.append(Triple(drug_id, "TREAT", disease_vocabulary_name_code.diz[possible_disease]))
    return list_of_indication