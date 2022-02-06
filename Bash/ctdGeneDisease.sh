#!/bin/sh

# Load Variable File
source ./variable.sh


CTDGENEDISEASE_PYTHON_FILE="../PreProcessing/ctdGeneDisease.py"

OUTPUT_PATH="../Result_PreProcessing/CTD_Gene_Disease_association.tsv"

THRESHOLD=70.78 # =percentile(data,90) preprocessed before

python3 ${CTDGENEDISEASE_PYTHON_FILE} \
 -C ${CTD_GENES_DISEASES_DB} \
 -O ${OUTPUT_PATH} \
 -T ${THRESHOLD}

