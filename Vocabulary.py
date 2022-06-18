import csv
from xmlrpc.client import Boolean


class Vocabulary:
    dict_id_to_name = {}
    dict_name_to_id = {}
   

    def __init__(self, path,vocabulary):
        if(path != None):
            print(path)
            with open(path) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    #Need to improve this, field have to be expressed in config file
                    id = row[vocabulary]
                    syn = row['Synonyms']
                    final = []
                    for item in syn.split("|"):
                        name = item.upper().strip()
                        final.append(name)
                        self.dict_name_to_id[name] = id
                    self.dict_id_to_name[id] = final
        else:
            return


def lookUpVocabulary(Triple,Vocabularies,entityType,pendingList) -> Boolean:
    select = Vocabularies[entityType]
    #We check only if the id is present
    if(Triple.tail in select.dict_name_to_id):
        #print("found!")
        return True
    else:
        #we add to a pending list hoping one day we will have found that ID
        listo = pendingList[entityType]
        listo.append(Triple)
        pendingList[entityType] = listo
        return False
