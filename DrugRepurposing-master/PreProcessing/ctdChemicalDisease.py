import os.path as check
import argparse

from chemicalVocabulary import ChemicalVocabulary
from Triple import Triple
from support_function import save_list_triple, check_dir


def process_chemical_disease(chemical_vocabulary_path, chemical_disease_path, output_path, threshold):
    chemical_vocabulary = ChemicalVocabulary(chemical_vocabulary_path)
    list_triple_chemical_disease = []

    print("Processing CTD Chemical-Disease")
    count = 1

    with open(chemical_disease_path) as file:
        for line in file:
            print("\rChemical - Disease n. " + f"{count:,}", end='') if count % 100000 == 0 else 0
            count += 1
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')

            chemical_id = 'MESH:' + sp_line[1]
            if chemical_id not in chemical_vocabulary.D_CHEMICAL:
                continue

            drugbank_id = chemical_vocabulary.D_CHEMICAL[chemical_id][0]
            disease_id = sp_line[4]
            inference_score = sp_line[7]

            if inference_score == "":  # No inference --> direct evidence
                list_triple_chemical_disease.append(Triple(drugbank_id, "TREAT", disease_id))
                continue
            else:
                inference_score = float(inference_score)
            # TODO Use Inference relation name Marker/Mechanism or Therapeutic or Both
            if inference_score >= threshold:
                list_triple_chemical_disease.append(Triple(drugbank_id, "TREAT", disease_id))

    print("\rChemical - Disease n. " + f"{count:,}")

    save_list_triple(output_path, list_triple_chemical_disease)


def main(args):
    chemical_disease_path = args["ctdchemicaldisease"]
    chemical_vocabulary_path = args["vocabulary"]
    output_path = args["output"]
    threshold = float(args["threshold"])

    if not check_dir(output_path):
        raise ValueError(output_path + " is Not a valid path")

    if not check.isfile(chemical_disease_path):
        raise ValueError(chemical_disease_path + " is Not a valid path")

    if not check.isfile(chemical_vocabulary_path):
        raise ValueError(chemical_vocabulary_path + " is Not a valid path")

    process_chemical_disease(chemical_vocabulary_path, chemical_disease_path, output_path, threshold)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="CTD Chemical Disease Parser")
    parser.add_argument("-C", "--ctdchemicaldisease", required=True, help="CTD Chemical Disease data file")
    parser.add_argument("-O", "--output", required=True, help="Chemical-Disease output data file")
    parser.add_argument("-T", "--threshold", required=True, help="Threshold 90° percentile for inference score")
    parser.add_argument("-V", "--vocabulary", required=True, help="Chemical Vocabulary")

    main(vars(parser.parse_args()))
