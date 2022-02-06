class DiseaseVocabularyNameCode:
    diz = {}

    def __init__(self, ctd_disease_path, omim_disease_path):

        with open(ctd_disease_path) as file:
            for line in file:
                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                chemical_name = sp_line[0].upper().strip()
                chemical_id_mesh = sp_line[1]

                if chemical_name and chemical_id_mesh:
                    self.diz[chemical_name] = chemical_id_mesh

        file.close()

        with open(omim_disease_path) as file:
            for line in file:
                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                mim_id = "OMIM:" + sp_line[1]
                preferred_title = [x.strip().upper() for x in sp_line[2].split(";")]
                alternative_titles = [x.strip().upper() for x in sp_line[3].split(";")]

                for name in preferred_title + alternative_titles:
                    if name:
                        if name not in self.diz:
                            self.diz[name] = mim_id
        file.close()
