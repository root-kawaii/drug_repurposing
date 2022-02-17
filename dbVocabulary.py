import csv


class DrugBankVocabulary:
    dict_id_to_name = {}
    dict_name_to_id = {}


    def __init__(self, path):
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                drug_id = row['DrugBank ID']
                drug_syn = row['Synonyms']
                final = []
                for item in drug_syn.split("|"):
                    name = item.upper().strip()
                    final.append(name)
                    self.dict_name_to_id[name] = drug_id
                self.dict_id_to_name[drug_id] = final
