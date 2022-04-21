#!/bin/sh

# Load Variable File
source ./variable.sh


WEBSITE="http://ctdbase.org/reports/"
GZ_EXTENSION=".gz"

# Create missing folders, if not already exist
mkdir -p ${DB_CTD_DIR}

# Chemical–gene interactions
CG="CTD_chem_gene_ixns.tsv"

# Chemical Gene Interaction type
CG_IT="CTD_chem_gene_ixn_types.tsv"

# Chemical GO Enriched Association
CGO="CTD_chem_go_enriched.tsv"

# Chemical Pathway association
CPW="CTD_chem_pathways_enriched.tsv"

# Gene Pathway association
GPW="CTD_genes_pathways.tsv"

# Disease–pathway associations
DPW="CTD_diseases_pathways.tsv"

# Chemical–phenotype interactions
CPH="CTD_pheno_term_ixns.tsv"

# Phenotype (GO)–Disease Inference Networks

#Pathway vocabulary



# What I want to download of CTD
downloads=(
    ${CTD_CHEMICALS_DB}
    ${CTD_DISEASES_DB}
    ${CTD_GENES_DB}
    ${CTD_GENES_DISEASES_DB}
    ${CTD_CHEMICALS_DISEASES_DB}
)

for FILE in "${downloads[@]}"; do
    if [[ -f "${FILE}" ]]; then
        echo "$FILE exist"
    else
        # String manipulation
        end=${FILE##*/}
        INDEX=$((${#FILE} - ${#end}))
        FILE=${FILE:INDEX}

        # Download showing only the progress bar, unzip and delete the zipped file
        wget -P ${DB_CTD_DIR}  ${WEBSITE}${FILE}${GZ_EXTENSION} -q --show-progress
        gunzip ${DB_CTD_DIR}${FILE}
    fi
done

