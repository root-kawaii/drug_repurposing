import argparse
import os.path as check

from Triple import Triple
from support_function import save_list_triple, check_dir


def process_gene_disease(gene_disease_path, output_path, threshold):

    list_triple_gene_disease = []

    print("Processing CTD Gene-Disease")
    count = 0

    with open(gene_disease_path) as in_f:
        for line in in_f:
            print("\rGene - Disease n. " + f"{count:,}", end='') if count % 100000 == 0 else 0
            count += 1
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')

            # gene_symbol = sp_line[0]
            gene_id = "GENEID:" + sp_line[1]
            # disease_name = sp_line[2]
            disease_id = sp_line[3]
            direct_evidence = sp_line[4]
            # inference_chemical_name = sp_line[5]

            if direct_evidence:
                list_triple_gene_disease.append(Triple(gene_id, "ISASSOCIATED", disease_id))
                continue

            inference_score = float(sp_line[6])

            # TODO Maybe we can use the inference chemical name field as relation in addition to direct evidence type..?

            if inference_score >= threshold:
                list_triple_gene_disease.append(Triple(gene_id, "ISASSOCIATED", disease_id))

    print("\rGene - Disease n. " + f"{count:,}")
    save_list_triple(output_path, list_triple_gene_disease)


def main(args):
    gene_disease_path = args["ctdgenedisease"]
    output_path = args["output"]
    threshold = float(args["threshold"])

    if not check_dir(output_path):
        raise ValueError(output_path + " is Not a valid path")

    if not check.isfile(gene_disease_path):
        raise ValueError(gene_disease_path + " is Not a valid path")

    process_gene_disease(gene_disease_path, output_path, threshold)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="CTD Gene Disease Parser")
    parser.add_argument("-C", "--ctdgenedisease", required=True, help="CTD Gene Disease data file")
    parser.add_argument("-O", "--output", required=True, help="Protein-Gene output data file")
    parser.add_argument("-T", "--threshold", required=True, help="Threshold 90° percentile for inference score")

    main(vars(parser.parse_args()))
