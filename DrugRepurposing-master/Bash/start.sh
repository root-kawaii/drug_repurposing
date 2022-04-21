#!/bin/sh

# Load Variable File
source ./variable.sh

# Exit when any command fails
set -e

# Create missing folders, if not already exist
mkdir -p ../KnowledgeGraph/
mkdir -p ../Result_PreProcessing/
mkdir -p ../Result_Embedding/

# |---> CTD
sh downloadDataBase.sh

# Download DataBase not downloadable
sh checkDB.sh

# Parse DrugBank
sh drugBank.sh -v
sh drugBank.sh -i
sh drugBank.sh -d

# Parse UniProt
sh uniProt.sh

# CTD - Disease Parent Disease
sh ctdParentDisease.sh

# CTD - Gene Disease
sh ctdGeneDisease.sh

# CTD - Chemical Disease
sh ctdChemicalDisease.sh

# Create Knowledge Graph --> Should be the last thing to do for pre processing
sh knowledgeGraph.sh
