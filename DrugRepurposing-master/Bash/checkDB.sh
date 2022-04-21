#!/bin/sh

# Load Variable File
source ./variable.sh

# List of DB to be checked
database=(
    ${DRUGBANK_DB}
    ${OMIM_DB}
    ${UNIPROT_DB}
    ${CTD_CHEMICALS_DB}
    ${CTD_DISEASES_DB}
    ${CTD_GENES_DB}
    ${CTD_CHEMICALS_DISEASES_DB}
    ${CTD_GENES_DISEASES_DB}
)

for FILE in "${database[@]}"; do
    if [[ -f "${FILE}" ]]; then
        echo "$FILE --> Exist"
    else
        echo "$FILE --> Not Exist"
        exit -1
    fi
done