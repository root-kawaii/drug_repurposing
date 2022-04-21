import csv
from xmlrpc.client import Boolean


class Vocabulary:
    dict_id_to_name = {}
    dict_name_to_id = {}
   

    def __init__(self, path):
        if(path != None):
            print(path)
            with open(path) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    #Need to improve this, field have to be expressed in config file
                    id = row['DrugBank ID']
                    syn = row['Synonyms']
                    final = []
                    for item in syn.split("|"):
                        name = item.upper().strip()
                        final.append(name)
                        self.dict_name_to_id[name] = id
                    self.dict_id_to_name[id] = final


def lookUpVocabulary(entity,Vocabularies,entityType) -> Boolean:
    select = Vocabularies[entityType]
    if(select.dict_name_to_id[entity]):
        print("found!")
        return True
    else:
         return False
