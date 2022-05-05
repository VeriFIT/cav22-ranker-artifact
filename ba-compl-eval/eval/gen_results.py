#!/usr/bin/env python3

# generation of results for the CAV'22 tool paper artifact

import math

from buchi_aux import *            # auxiliary functions for Buchi automata benchmarks

################### SETTINGS ###########################

# in seconds
TIMEOUT = 300
TIMEOUT_VAL = TIMEOUT * 1.1

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

# compute summaries
df_summary_random = summary_stats(df_random)
df_summary_ltl = summary_stats(df_ltl)
df_summary_automizer = summary_stats(df_automizer)
df_summary_all = summary_stats(df_all)


# sanitize the data frames
df_random = sanitize_results(df_random, df_summary_all, TIMEOUT_VAL)
df_ltl = sanitize_results(df_ltl, df_summary_all, TIMEOUT_VAL)
df_automizer = sanitize_results(df_automizer, df_summary_all, TIMEOUT_VAL)
df_all = sanitize_results(df_all, df_summary_all, TIMEOUT_VAL)

# plot graphs for ranker/rankerOld  and ranker/spot
scatplot3(df_random, df_ltl, df_automizer, {'x': "ranker-autfilt", 'y': "ranker-tacas22-autfilt",
                                            'xname': "Ranker", 'yname': "OldRanker", 'max': 3000}, save=True)
scatplot3(df_random, df_ltl, df_automizer, {'x': "ranker-autfilt", 'y': "spot-autfilt", 'max': 3000,
                                            'xname': "Ranker", 'yname': "Spot"}, save=True)


print("\n")
print("######################################################################################################")
print("####                                     Tables 2 & 3  - random                                   ####")
print("######################################################################################################")
print_win_table(df_random, df_summary_random, "ranker")
print("\n")

print("######################################################################################################")
print("####                                     Tables 2 & 3  - LTL                                      ####")
print("######################################################################################################")
print_win_table(df_ltl, df_summary_ltl, "ranker")
print("\n")

print("######################################################################################################")
print("####                                     Tables 2 & 3  - Automizer                                ####")
print("######################################################################################################")
print_win_table(df_automizer, df_summary_automizer, "ranker")
print("\n")

print("######################################################################################################")
print("####                                     Tables 2 & 3  - all                                      ####")
print("######################################################################################################")
print_win_table(df_all, df_summary_all, "ranker")
print("\n")

################################################################
####   Inherently weak and semi-determinstic optimizations
################################################################

# reload the inputs
df_ltl = load_results(FILENAME_ltl)
df_automizer = load_results(FILENAME_automizer)

df_ltl = connect_with_classification(df_ltl, CLASSIFICATION_ltl)
df_automizer = connect_with_classification(df_automizer, CLASSIFICATION_automizer)

# remove timeouts where ranker finished and autfilt didn't  -- we are removing
# these to not skew the results because autfilt could not successfully do its
# --high reduction
remove_auts_automizer = [
  "automata/advanced-automata-for-termination-red/AliasDarteFeautrierGonnord-SAS2010-Fig2b_true-termination.c_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/AliasDarteFeautrierGonnord-SAS2010-nestedLoop_true-termination_true-no-overflow.c_Iteration5_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/BrockschmidtCookFuhs-2013CAV-Fig1-alloca_true-termination.c.i_Iteration2_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/BrockschmidtCookFuhs-2013CAV-Fig1-alloca_true-termination.c.i_Iteration3_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/ComplxStruc_false-termination.c_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/CookSeeZuleger-2013TACAS-Fig7b-alloca_true-termination.c.i_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/CookSeeZuleger-2013TACAS-Fig7b-alloca_true-termination.c.i_Iteration6_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/LarrazOliverasRodriguez-CarbonellRubio-FMCAD2013-Fig1_true-termination_true-no-overflow.c_Iteration3_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/LarrazOliverasRodriguez-CarbonellRubio-FMCAD2013-Fig1_true-termination_true-no-overflow.c_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2-TACAS2011-Fig3_true-termination.c_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2-TACAS2011-Fig3_true-termination.c_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2-TACAS2011-Fig3_true-termination.c_Iteration5_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2_true-termination.c_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2_true-termination.c_Iteration6_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2_true-termination.c_Iteration6_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-LICS2004-Fig2_true-termination.c_Iteration7_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-TACAS2011-Fig3_true-termination.c_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-TACAS2011-Fig3_true-termination.c_Iteration6_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-TACAS2011-Fig3_true-termination.c_Iteration6_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/PodelskiRybalchenko-TACAS2011-Fig3_true-termination.c_Iteration7_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/TelAviv-Amir-Minimum-alloca_true-termination.c.i_Iteration4_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/TelAviv-Amir-Minimum-alloca_true-termination.c.i_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/TelAviv-Amir-Minimum-alloca_true-termination.c.i_Iteration5_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/TelAviv-Amir-Minimum_true-termination_true-valid-memsafety.c_Iteration3_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/TelAviv-Amir-Minimum_true-termination_true-valid-memsafety.c_Iteration4_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/TelAviv-Amir-Minimum_true-termination_true-valid-memsafety.c_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/UpAndDown_false-termination_true-no-overflow.c_Iteration15_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/UpAndDown_false-termination_true-no-overflow.c_Iteration16_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/UpAndDown_false-termination_true-no-overflow.c_Iteration3_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/Urban-alloca_true-termination.c.i_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/Urban-alloca_true-termination.c.i_Iteration6_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/b.11-alloca_true-termination_true-no-overflow.c.i_Iteration3_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/b.11-alloca_true-termination_true-no-overflow.c.i_Iteration4_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/b.11-alloca_true-termination_true-no-overflow.c.i_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/b.11-alloca_true-termination_true-no-overflow.c.i_Iteration5_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/b.15-alloca_true-termination_true-no-overflow.c.i_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/c.02-alloca_true-termination_true-no-overflow.c.i_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/c.03-alloca_true-termination_true-no-overflow.c.i_Iteration4_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/c.03-alloca_true-termination_true-no-overflow.c.i_Iteration4_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/c.08-alloca_true-termination_true-no-overflow.c.i_Iteration3_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/exp10.hoa",
  "automata/advanced-automata-for-termination-red/exp105.hoa",
  "automata/advanced-automata-for-termination-red/exp11.hoa",
  "automata/advanced-automata-for-termination-red/exp24.hoa",
  "automata/advanced-automata-for-termination-red/exp38.hoa",
  "automata/advanced-automata-for-termination-red/exp59.hoa",
  "automata/advanced-automata-for-termination-red/exp6.hoa",
  "automata/advanced-automata-for-termination-red/exp67.hoa",
  "automata/advanced-automata-for-termination-red/exp69.hoa",
  "automata/advanced-automata-for-termination-red/exp91.hoa",
  "automata/advanced-automata-for-termination-red/java_Continue1-alloca_true-termination.c.i_Iteration12_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/lis-alloca_true-termination.c.i_Iteration12_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/lis-alloca_true-termination.c.i_Iteration5_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/min_rf_true-termination.c_Iteration3_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/min_rf_true-termination.c_Iteration4_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/s3_clnt_3.cil_true-unreach-call_true-termination.c_Iteration2_B.ba.hoa",
  "automata/advanced-automata-for-termination-red/s3_srvr_1a_true-unreach-call_false-termination.cil.c_Iteration15_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/s3_srvr_1a_true-unreach-call_false-termination.cil.c_Iteration3_A.ba.hoa",
  "automata/advanced-automata-for-termination-red/s3_srvr_1a_true-unreach-call_false-termination.cil.c_Iteration3_B.ba.hoa",
]

# remove the unfinished automata
df_automizer_opt = df_automizer[~df_automizer["name"].isin(remove_auts_automizer)]

# get IW and SDBA automata
get_iw_auts = lambda df: df[df['inherently weak'] == 1].copy(deep=True)
get_sdba_auts = lambda df: df[(df['inherently weak'] == 0) & (df['semi deterministic'] == 1)].copy(deep=True)

df_iw_automizer = get_iw_auts(df_automizer_opt)
df_iw_ltl = get_iw_auts(df_ltl)
df_iw_all = pd.concat([df_iw_ltl,df_iw_automizer])
print(f'! # of IW automata from df_automizer: {len(df_iw_automizer)}')
print(f'! # of IW automata from df_ltl: {len(df_iw_ltl)}')
print(f'! # of IW automata from ALL: {len(df_iw_all)}')

df_sdba_automizer = get_sdba_auts(df_automizer_opt)
df_sdba_ltl = get_sdba_auts(df_ltl)
df_sdba_all = pd.concat([df_sdba_ltl,df_sdba_automizer])
print(f'! # of SDBA automata from df_automizer: {len(df_sdba_automizer)}')
print(f'! # of SDBA automata from df_ltl: {len(df_sdba_ltl)}')
print(f'! # of SDBA automata from ALL: {len(df_sdba_all)}')

# compute statistics of the experiments
df_summary_iw_automizer = summary_stats(df_iw_automizer)
df_summary_iw_ltl = summary_stats(df_iw_ltl)
df_summary_iw_all = summary_stats(df_iw_all)
df_summary_sdba_automizer = summary_stats(df_sdba_automizer)
df_summary_sdba_ltl = summary_stats(df_sdba_ltl)
df_summary_sdba_all = summary_stats(df_sdba_all)

print("\n")
print("######################################################")
print("####              Table 1 top - LTL               ####")
print("######################################################")
print_opt_table(df_iw_ltl, df_summary_iw_ltl, [("ranker", "MiHay-prune"), ("ranker-iw-orig", "MiHay")])

print("\n")
print("######################################################")
print("####              Table 1 top - Automizer         ####")
print("######################################################")
print_opt_table(df_iw_automizer, df_summary_iw_automizer, [("ranker", "MiHay-prune"), ("ranker-iw-orig", "MiHay")])

print("\n")
print("######################################################")
print("####              Table 1 top - all               ####")
print("######################################################")
print_opt_table(df_iw_all, df_summary_iw_all, [("ranker", "MiHay-prune"), ("ranker-iw-orig", "MiHay")])
print("\n")

print("######################################################")
print("####              Table 1 bottom - LTL            ####")
print("######################################################")
print_opt_table(df_sdba_ltl, df_summary_sdba_ltl, [("ranker", "NCSB-MaxRank"), ("ranker-sd-ncsb-lazy", "NCSB-Lazy")])

print("\n")
print("######################################################")
print("####              Table 1 bottom - Automizer      ####")
print("######################################################")
print_opt_table(df_sdba_automizer, df_summary_sdba_automizer, [("ranker", "NCSB-MaxRank"), ("ranker-sd-ncsb-lazy", "NCSB-Lazy")])

print("\n")
print("######################################################")
print("####              Table 1 bottom - all            ####")
print("######################################################")
print_opt_table(df_sdba_all, df_summary_sdba_all, [("ranker", "NCSB-MaxRank"), ("ranker-sd-ncsb-lazy", "NCSB-Lazy")])
print("\n")

# sanitize
df_iw_ltl = sanitize_results(df_iw_ltl, df_summary_iw_all, TIMEOUT_VAL)
df_iw_automizer = sanitize_results(df_iw_automizer, df_summary_iw_all, TIMEOUT_VAL)
df_sdba_ltl = sanitize_results(df_sdba_ltl, df_summary_sdba_all, TIMEOUT_VAL)
df_sdba_automizer = sanitize_results(df_sdba_automizer, df_summary_sdba_all, TIMEOUT_VAL)

# and plot...
scatplot2(df_iw_automizer, df_iw_ltl, {'x': "ranker-nopost", 'y': "ranker-iw-orig-nopost",
                                       'xname': "MiHay-Prune", 'yname': "MiHay", 'max': 15000}, color1='green', color2='red', save=True)
scatplot2(df_sdba_automizer, df_sdba_ltl, {'x': "ranker-nopost", 'y': "ranker-sd-ncsb-lazy-nopost",
                                           'xname': "NCSB-MaxRank", 'yname': "NCSB-Lazy", 'max': 15000}, color1='green', color2='red', save=True)
