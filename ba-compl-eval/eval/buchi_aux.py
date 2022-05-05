#!/usr/bin/env python3
#
# auxiliary functions for results of Buchi automata benchmarks

import evallib as el               # this contains auxiliary functionality for evaluation of experiments

# Connect a DF with results to DF with classification of inputs
def connect_with_classification(df, clas_file):
    df_clas = el.read_file(clas_file)
    df = pd.merge(df, df_clas, on='name')
    return df


# prints results of classification
def print_classification(df):
    df_empty = df[df['empty'] == 1]
    df_deterministic = df[df['deterministic'] == 1]
    df_deterministic_weak = df[(df['deterministic'] == 1) & (df['weak'] == 1)]
    df_inherently_weak = df[df['inherently weak'] == 1]
    df_semi_deterministic = df[df['semi deterministic'] == 1]
    df_semi_not_iw = df[(df['semi deterministic'] == 1) & (df['inherently weak'] == 0)]
    df_terminal = df[df['terminal'] == 1]
    df_unambiguous = df[df['unambiguous'] == 1]
    df_weak = df[df['weak'] == 1]
    df_very_weak = df[df['very weak'] == 1]
    df_elevator = df[df['elevator'] == 1]
    df_elevator_not_semi = df[(df['elevator'] == 1) & (df['semi deterministic'] == 0)]
    df_one_state = df[df['one-state'] == 1]

    print(f"! Classification of input automata")
    print(f"!   # empty: {len(df_empty)}")
    print(f"!   # deterministic: {len(df_deterministic)}")
    print(f"!   # deterministic weak: {len(df_deterministic_weak)}")
    print(f"!   # inherently weak: {len(df_inherently_weak)}")
    print(f"!   # semi-deterministic: {len(df_semi_deterministic)}")
    print(f"!   # semi-deterministic-not-iw: {len(df_semi_not_iw)}")
    print(f"!   # terminal: {len(df_terminal)}")
    print(f"!   # unambiguous: {len(df_unambiguous)}")
    print(f"!   # weak: {len(df_weak)}")
    print(f"!   # very weak: {len(df_very_weak)}")
    print(f"!   # elevator: {len(df_elevator)}")
    print(f"!   # elevator not semi-deterministic: {len(df_elevator_not_semi)}")
    print(f"!   # one-state: {len(df_one_state)}")


# remove too easy automata from processing
def filter_non_easy(df):
    # sanitization based on properties of input automata
    df = df[df['one-state'] == 0]
   # df = df[df['semi deterministic'] == 0]
   # df = df[df['inherently weak'] == 0]
   # df = df[df['unambiguous'] == 0]
    return df

# computes summary statistics
def summary_stats(df):
  summary = dict()
  for col in df.columns:
      if re.search('-States$', col) or re.search('-runtime$', col):
          summary[col] = dict()
          summary[col]['max'] = df[col].max()
          summary[col]['min'] = df[col].min()
          summary[col]['mean'] = df[col].mean()
          summary[col]['median'] = df[col].median()
          summary[col]['std'] = df[col].std()
          summary[col]['timeouts'] = df[col].isna().sum()
  return pd.DataFrame(summary).transpose()


# table to LaTeX file
def table_to_file(table, headers, out_file):
    with open(f"plots/{out_file}.tex", mode='w') as fl:
        print(tab.tabulate(table, headers=headers, tablefmt="latex"), file=fl)

# load results
def load_results(filename):
    df = el.read_file(filename)

    print(f"! Loaded results")
    print(f"!   file:  {filename}")
    print(f"!   time:  {datetime.datetime.now()}")
    print(f"!   # of automata: {len(df)}")
    return df
