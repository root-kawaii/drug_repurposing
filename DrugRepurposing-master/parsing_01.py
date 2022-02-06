import xml.etree.ElementTree as Tree
import spacy
import argparse
import os.path as check

def parsing(drug_id,target) #dictionary) -> []:


    interactions = []

    for drug in drug_id[0]:
        actions = set([])
        drug_interaction = target.findall("specified_interaction")

        if drug_interaction:
            id_target = target.findall("specified_interaction")[0].attrib.get("id")#if i can find said relation otherwise loop over all
                                                                                   #entities (?)
        else:
            name = target.findall("everything else")[0].text #every other entity
            try:
                if(dictionary != None)
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