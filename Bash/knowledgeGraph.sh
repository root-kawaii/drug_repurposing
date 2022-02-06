#!/bin/sh

# Load Variable File
source ./variable.sh


KG_PYTHON_FILE="../PreProcessing/knowledgeGraph.py"

PRE_PROCESSING_RESULT="../Result_PreProcessing/"
KG_RESULT="../KnowledgeGraph/"

# % of Train and Validation. Test = 1 - Train - Validation
PERC_TRAIN=0.6
PERC_VALID=0.2

python3 ${KG_PYTHON_FILE} \
-P ${PRE_PROCESSING_RESULT} \
-F ${KG_RESULT} \
-T ${PERC_TRAIN} \
-V ${PERC_VALID}