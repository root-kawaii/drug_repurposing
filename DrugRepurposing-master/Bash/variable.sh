#!/bin/sh

# DataBase Directory
DB_DIR="../DataBase/"
DB_UNIPROT_DIR="${DB_DIR}UNIPROT/"
DB_DRUGBANK_DIR="${DB_DIR}DRUGBANK/"
DB_CTD_DIR="${DB_DIR}CTD/"
DB_OMIM_DIR="${DB_DIR}OMIM/"

# DataBase File
DRUGBANK_DB="${DB_DRUGBANK_DIR}DrugBank.xml"

OMIM_DB="${DB_OMIM_DIR}mimTitles.txt"

UNIPROT_DB="${DB_UNIPROT_DIR}UniProt.tsv"

CTD_CHEMICALS_DB="${DB_CTD_DIR}CTD_chemicals.tsv"
CTD_DISEASES_DB="${DB_CTD_DIR}CTD_diseases.tsv"
CTD_GENES_DB="${DB_CTD_DIR}CTD_genes.tsv"

CTD_CHEMICALS_DISEASES_DB="${DB_CTD_DIR}CTD_chemicals_diseases.tsv"
CTD_GENES_DISEASES_DB="${DB_CTD_DIR}CTD_genes_diseases.tsv"

DRUGBANK_VOCABULARY_PATH="${DB_DRUGBANK_DIR}/DrugBank_Vocabulary.csv"

# Function
load_bash_profile(){
if [[ -f ~/.bash_profile ]]; then
	. ~/.bash_profile
fi
}





