#!/usr/bin/env bash

# Load Variable File
source ./variable.sh


TRAIN_PYTHON_FILE="../Embedding/train_kg.py"



PYTHONPATH=.. python3 ${TRAIN_PYTHON_FILE}
