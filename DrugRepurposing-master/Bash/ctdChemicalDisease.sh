#!/bin/sh

# Load Variable File
source ./variable.sh

CTDCHEMICALDISEASE_PYTHON_FILE="../PreProcessing/ctdChemicalDisease.py"

OUTPUT_PATH="../Result_PreProcessing/CTD_Chemical_Disease_association.tsv"

THRESHOLD=45.62 # =percentile(data,90) preprocessed before


python3 ${CTDCHEMICALDISEASE_PYTHON_FILE} \
 -C ${CTD_CHEMICALS_DISEASES_DB} \
 -O ${OUTPUT_PATH} \
 -V ${CTD_CHEMICALS_DB} \
 -T ${THRESHOLD}

