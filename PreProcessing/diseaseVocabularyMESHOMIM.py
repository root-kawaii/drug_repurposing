from enum import Enum
import argparse
import os.path as check

from Triple import Triple
from support_function import save_list_triple, check_dir


class ID(Enum):
    MESH = 0
    OMIM = 1


class DiseaseVocabularyMESHOMIM:
    D_OMIM = {}
    D_MESH = {}
    TRIPLE_PARENTS = []

    def create_vocabulary(self, disease_vocabulary_path):
        with open(disease_vocabulary_path) as in_f:
            for line in in_f:
                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                diseaseName = sp_line[0]
                disease_id = sp_line[1]
                alt_disease_ids = sp_line[2]
                definition = sp_line[3]
                parentIDs = sp_line[4]
                treeNumbers = sp_line[5]
                parentTreeNumbers = sp_line[6]
                synonyms = sp_line[7]
                slimMapping = sp_line[8]

                type_id = self.parse_type_id(disease_id)
                if type_id == ID.MESH:
                    self.D_MESH[disease_id] = set([])
                elif type_id == ID.OMIM:
                    self.D_OMIM[disease_id] = set([])

                list_alternatives = self.parse_alternative_disease_id(alt_disease_ids)

                for alternative in list_alternatives:
                    if type_id == ID.MESH:
                        self.D_MESH[disease_id].add(alternative)
                    elif type_id == ID.OMIM:
                        self.D_OMIM[disease_id].add(alternative)

                    alternative_type = self.parse_type_id(alternative)

                    if alternative_type == ID.MESH and alternative not in self.D_MESH:
                        self.D_MESH[alternative] = set([])
                    elif alternative_type == ID.OMIM and alternative not in self.D_OMIM:
                        self.D_OMIM[alternative] = set([])

                    if alternative_type == ID.MESH:
                        self.D_MESH[alternative].add(disease_id)
                    elif alternative_type == ID.OMIM:
                        self.D_OMIM[alternative].add(disease_id)

    def parse_type_id(self, name) -> ID:
        if name.find("MESH") >= 0:
            return ID.MESH
        elif name.find("MIM") >= 0:
            return ID.OMIM

    def parse_alternative_disease_id(self, alt_disease_ids) -> []:
        alternatives = alt_disease_ids.split("|")
        if alternatives:
            for a in alternatives:
                if a.find("OMIM") >= 0:
                    continue
                elif a.find("MESH") >= 0:
                    continue
                else:
                    alternatives.remove(a)
            return alternatives
        else:
            return None

    def create_triple_parent(self, disease_vocabulary_path, disease_parent_disease_path):
        with open(disease_vocabulary_path) as in_f:
            for line in in_f:
                if line.startswith('#'):
                    continue
                sp_line = line.strip('\n').split('\t')

                disease_id = sp_line[1]
                parent_ids = sp_line[4]

                parents_list = self.parse_alternative_disease_id(parent_ids)

                for parent in parents_list:
                    self.TRIPLE_PARENTS.append(Triple(parent, "ISPARENTOF", disease_id))

        save_list_triple(disease_parent_disease_path, self.TRIPLE_PARENTS)


def main(args):
    parent_path = args["parent"]
    disease_vocabulary_path = args["diseasevocabularypath"]

    print("Create Disease Parent Disease")

    if not check.isfile(disease_vocabulary_path):
        raise ValueError(disease_vocabulary_path + " is Not a valid path")

    if not check_dir(parent_path):
        raise ValueError(parent_path + " is Not a valid path")

    vocabulary = DiseaseVocabularyMESHOMIM()
    vocabulary.create_triple_parent(disease_vocabulary_path, parent_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="Disease Parent Creator")
    parser.add_argument("-P", "--parent", required=True, help="Disease parent disease output data file")
    parser.add_argument("-V", "--diseasevocabularypath", required=True, help="Disease Vocabulary data file")

    main(vars(parser.parse_args()))
