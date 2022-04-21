#!/bin/sh

# Load Variable File
source ./variable.sh


UNIPROT_PYTHON_FILE="../PreProcessing/uniProt.py"


UNIPROT_ENCODING_PATH="../Result_PreProcessing/UniProt_Protein_Gene_Encoding.tsv"
UNIPROT_INTERACTION_PATH="../Result_PreProcessing/UniProt_Protein_Protein_Interaction.tsv"
UNIPROT_DISEASE_PATH="../Result_PreProcessing/UniProt_Protein_Disease_Association.tsv"


python3 ${UNIPROT_PYTHON_FILE} \
 -P ${UNIPROT_DB} \
 -I ${UNIPROT_INTERACTION_PATH} \
 -E ${UNIPROT_ENCODING_PATH} \
 -D ${UNIPROT_DISEASE_PATH} \
 -V ${CTD_DISEASES_DB} \
 -G ${CTD_GENES_DB} \
 -O ${OMIM_DB} \
 -C ${DRUGBANK_VOCABULARY_PATH}



