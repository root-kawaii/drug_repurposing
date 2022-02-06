class ChemicalVocabulary:
    D_CHEMICAL = {}

    def __init__(self,  chemical_vocabulary_path):
        with open(chemical_vocabulary_path) as in_f:
            for line in in_f:
                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                chemical_id = sp_line[1]
                drugbank_ids = sp_line[8]
                if len(drugbank_ids) > 0:
                    drugbank_ids = drugbank_ids.split('|')
                    self.D_CHEMICAL[chemical_id] = drugbank_ids
