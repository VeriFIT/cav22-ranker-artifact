#!/usr/bin/env python3

# generation of results for the CAV'22 tool paper artifact

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

# load results and connect with classification
df_random = load_results(FILENAME_random)
df_ltl = load_results(FILENAME_ltl)
df_automizer = load_results(FILENAME_automizer)

df_random = connect_with_classification(df_random, CLASSIFICATION_random)
print_classification(df_random, "random")
df_ltl = connect_with_classification(df_ltl, CLASSIFICATION_ltl)
print_classification(df_ltl, "ltl")
df_automizer = connect_with_classification(df_automizer, CLASSIFICATION_automizer)
print_classification(df_automizer, "automizer")

# filter only non-easy automata
df_random = filter_non_easy(df_random)
print(f'! # of automata from random after sanitization: {len(df_random)}')
df_ltl = filter_non_easy(df_ltl)
print(f'! # of automata from ltl after sanitization: {len(df_ltl)}')
df_automizer = filter_non_easy(df_automizer)
print(f'! # of automata from automizer after sanitization: {len(df_automizer)}')
df_all = pd.concat([df_random, df_ltl, df_automizer])
print(f'! # of automata from ALL after sanitization: {len(df_all)}')

df_summary_random = summary_stats(df_random)
df_summary_ltl = summary_stats(df_ltl)
df_summary_automizer = summary_stats(df_automizer)
df_summary_all = summary_stats(df_all)


################  states of complements ##################
interesting = [
               # "ranker-nopost",
               "ranker-autfilt",
               # "ranker-tacas22-nopost",
               "ranker-tacas22-autfilt",
               # "schewe",
               "piterman-autfilt",
               "safra-autfilt",
               "spot-autfilt",
               "fribourg-autfilt",
               "ltl2dstar-autfilt",
               "seminator-autfilt",
               "roll-autfilt",
              ]

df_summary_random.loc[[x + '-States' for x in interesting]]
