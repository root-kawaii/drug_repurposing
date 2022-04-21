#!/bin/sh

# Load Variable File
source ./variable.sh


PARENT_PYTHON_FILE="../PreProcessing/diseaseVocabularyMESHOMIM.py"

PARENT_DISEASE_PATH="../Result_PreProcessing/CTD_Disease_Disease_Parent.tsv"

python3 ${PARENT_PYTHON_FILE} \
 -P ${PARENT_DISEASE_PATH} \
 -V ${CTD_DISEASES_DB}

