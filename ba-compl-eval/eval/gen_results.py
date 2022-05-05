#!/usr/bin/env python3

# generation of results for the CAV'22 tool paper artifact

import re as re
import tabulate as tab
import math

from buchi_aux import *            # auxiliary functions for Buchi automata benchmarks

################### SETTINGS ###########################

# in seconds
TIMEOUT = 300
TIMEOUT_VAL = TIMEOUT * 1.1
TIME_MIN = 0.01

AUTOMATA_DIR="../automata"

FILENAME_random = "./random-to60.csv"
CLASSIFICATION_random = AUTOMATA_DIR + "/random-all-classification.csv"

FILENAME_ltl = "./ltl-to60.csv"
CLASSIFICATION_ltl = AUTOMATA_DIR + "/from_ltl_classification.csv"

FILENAME_automizer = "./automizer-to60.csv"
CLASSIFICATION_automizer = AUTOMATA_DIR + "/advanced-automata-classification.csv"

######################

df_random = load_results(FILENAME_random)
df_ltl = load_results(FILENAME_ltl)
df_automizer = load_results(FILENAME_automizer)

df_random = connect_with_classification(df_random, CLASSIFICATION_random)
print_classification(df_random)
df_ltl = connect_with_classification(df_ltl, CLASSIFICATION_ltl)
print_classification(df_ltl)
df_automizer = connect_with_classification(df_automizer, CLASSIFICATION_automizer)
print_classification(df_automizer)
