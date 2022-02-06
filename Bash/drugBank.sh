#!/bin/sh

# Load Variable File
source ./variable.sh


DRUGBANK_PYTHON_FILE="../PreProcessing/drugBank.py"


DRUGBANK_TARGET_PATH="../Result_PreProcessing/DrugBank_Drug_Target_Interaction.tsv"
DRUGBANK_DISEASE_PATH="../Result_PreProcessing/DrugBank_Drug_Disease_Indication.tsv"



while getopts vdi option
do
    case "${option}" in
        v) VOCABULARY="True";;
        d) DISEASE="True";;
        i) INTERACTION="True";;
    esac
done


if [[ ${VOCABULARY} = "True" ]]; then
    python3 ${DRUGBANK_PYTHON_FILE} \
    -P ${DRUGBANK_DB} \
    -V ${DRUGBANK_VOCABULARY_PATH}\
    -v
    exit 0
fi

if [[ ${DISEASE} = "True" ]]; then
    python3 ${DRUGBANK_PYTHON_FILE} \
    -P ${DRUGBANK_DB} \
    -D ${DRUGBANK_DISEASE_PATH} \
    -C ${CTD_DISEASES_DB} \
    -O ${OMIM_DB} \
    -d
    exit 0
fi

if [[ ${INTERACTION} = "True" ]]; then
    python3 ${DRUGBANK_PYTHON_FILE} \
    -P ${DRUGBANK_DB} \
    -I ${DRUGBANK_TARGET_PATH} \
    -V ${DRUGBANK_VOCABULARY_PATH} \
    -i
    exit 0
fi

