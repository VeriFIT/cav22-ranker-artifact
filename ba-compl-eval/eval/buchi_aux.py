#!/usr/bin/env python3
#
# auxiliary functions for results of Buchi automata benchmarks

import datetime
import pandas as pd
import re as re
import mizani.formatters as mizani
import plotnine as p9
import tabulate as tab

import evallib as el               # this contains auxiliary functionality for evaluation of experiments

# Connect a DF with results to DF with classification of inputs
def connect_with_classification(df, clas_file):
    df_clas = el.read_file(clas_file)
    df = pd.merge(df, df_clas, on='name')
    return df


# prints results of classification
def print_classification(df, dataset):
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

    print(f"! Classification of input automata for \"{dataset}\"")
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


def scatter_plot3(df1, df2, df3, xcol, ycol, domain, color1='black', color2='red', color3='green', xname=None, yname=None, log=False, width=6, height=6, clamp=True, tickCount=5):
    assert len(domain) == 2

    POINT_SIZE = 1.5
    DASH_PATTERN = (0, (6, 2))

    if xname is None:
        xname = xcol
    if yname is None:
        yname = ycol

    # formatter for axes' labels
    ax_formatter = mizani.custom_format('{:n}')

    if clamp:  # clamp overflowing values if required
        df1 = df1.copy(deep=True)
        df1.loc[df1[xcol] > domain[1], xcol] = domain[1]
        df1.loc[df1[ycol] > domain[1], ycol] = domain[1]

        df2 = df2.copy(deep=True)
        df2.loc[df2[xcol] > domain[1], xcol] = domain[1]
        df2.loc[df2[ycol] > domain[1], ycol] = domain[1]

        df3 = df3.copy(deep=True)
        df3.loc[df3[xcol] > domain[1], xcol] = domain[1]
        df3.loc[df3[ycol] > domain[1], ycol] = domain[1]

    # generate scatter plot
    scatter = p9.ggplot(df1)
    scatter += p9.aes(x=xcol, y=ycol)
    scatter += p9.geom_point(size=POINT_SIZE, na_rm=True, color=color1, alpha=0.5)
    scatter += p9.geom_point(size=POINT_SIZE, na_rm=True, data=df2, color=color2, alpha=0.5)
    scatter += p9.geom_point(size=POINT_SIZE, na_rm=True, data=df3, color=color3, alpha=0.5)
    scatter += p9.labs(x=xname, y=yname)

    # rug plots
    scatter += p9.geom_rug(na_rm=True, sides="tr", color=color1, alpha=0.05)
    scatter += p9.geom_rug(na_rm=True, sides="tr", data=df2, color=color2, alpha=0.05)
    scatter += p9.geom_rug(na_rm=True, sides="tr", data=df3, color=color3, alpha=0.05)

    if log:  # log scale
        scatter += p9.scale_x_log10(limits=domain, labels=ax_formatter)
        scatter += p9.scale_y_log10(limits=domain, labels=ax_formatter)
    else:
        scatter += p9.scale_x_continuous(limits=domain, labels=ax_formatter)
        scatter += p9.scale_y_continuous(limits=domain, labels=ax_formatter)

    # scatter += p9.theme_xkcd()
    scatter += p9.theme_bw()
    scatter += p9.theme(panel_grid_major=p9.element_line(color='#666666', alpha=0.5))
    scatter += p9.theme(panel_grid_minor=p9.element_blank())
    scatter += p9.theme(figure_size=(width, height))
    scatter += p9.theme(text=p9.element_text(size=24, color="black"))

    # generate additional lines
    scatter += p9.geom_abline(intercept=0, slope=1, linetype=DASH_PATTERN)  # diagonal
    scatter += p9.geom_vline(xintercept=domain[1], linetype=DASH_PATTERN)  # vertical rule
    scatter += p9.geom_hline(yintercept=domain[1], linetype=DASH_PATTERN)  # horizontal rule

    res = scatter

    return res

def scatplot3(df1, df2, df3, params, color1='blue', color2='red', color3='green', save=False):
    size = 8
    if 'xname' not in params:
        params['xname'] = None
    if 'yname' not in params:
        params['yname'] = None
    if 'max' not in params:
        params['max'] = 10000
    if 'min' not in params:
        params['min'] = 1
    if 'tickCount' not in params:
        params['tickCount'] = 5
    if 'filename' not in params:
        params['filename'] = "fig_" + params['x'] + "_vs_" + params['y'] + ".pdf"

    pl = scatter_plot3(df1, df2, df3,
                         xcol=params['x'] + '-States',
                         ycol=params['y'] + '-States',
                         xname=params['xname'], yname=params['yname'],
                         domain=[params['min'], params['max']],
                         tickCount=params['tickCount'],
                         color1=color1, color2=color2, color3=color3,
                         log=True, width=size, height=size)

    if save:
      pl.save(filename=params['filename'],
              dpi=1000)

    return pl


# sanitize results (substitute timeouts with TIMEOUT_VAL and 0 states with 1)
def sanitize_results(df, df_summary_states, timeout_val):
  TIME_MIN = 0.01
  # min and max states
  states_min = 1
  states_max = df_summary_states['max'].max()
  states_timeout = states_max * 1.1

  # sanitizing NAs
  for col in df.columns:
      if re.search('-States$', col):
          df[col].fillna(states_timeout, inplace=True)
          df[col].replace(0, states_min, inplace=True)  # to remove 0 (in case of log graph)

      if re.search('-runtime$', col):
          df[col].fillna(timeout_val, inplace=True)
          df.loc[df[col] < TIME_MIN, col] = TIME_MIN  # to remove 0 (in case of log graph)

  return df


# comparing wins/loses
def compute_wins(df, method):
  all_methods = [
                 "ranker",
                 "ranker-tacas22",
                 "piterman",
                 # "schewe",
                 "safra",
                 "spot",
                 "fribourg",
                 "ltl2dstar",
                 "seminator",
                 "roll",
                ]
  suffix = "-autfilt-States"
  method_suf = method + suffix
  all_methods_suf = [m + suffix for m in all_methods]

  states_timeout = df[all_methods_suf].max().max()

  compare_methods = []
  for m in all_methods_suf:
    if (m != method_suf):
      compare_methods += [(method_suf, m)]

#  compare_methods.append(("ranker-nopost-States", "ranker-maxr-nopost-States"))
#  compare_methods.append(("ranker-nopost-States", "schewe-States"))

  dict_wins = {}
  for left, right in compare_methods:
        left_over_right = df[df[left] < df[right]]
        right_timeouts = left_over_right[left_over_right[right] == states_timeout]

        right_over_left = df[df[left] > df[right]]
        left_timeouts = right_over_left[right_over_left[left] == states_timeout]

        dict_wins[right] = {'wins': len(left_over_right),
                            # 'winsTO': len(right_timeouts),
                            'losses': len(right_over_left),
                            # 'lossesTO': len(left_timeouts),
                           }
  return dict_wins

def print_win_table(df, df_summary, method):
  tab_wins = []
  method_name = method + "-autfilt-States"
  tab_wins.append([method,
                   df_summary.loc[method_name]["mean"],
                   df_summary.loc[method_name]["median"],
                   "",
                   # "",
                   "",
                   # "",
                   df_summary.loc[method_name]["timeouts"],
                  ])
  dict_wins = compute_wins(df, method)
  for key, val in dict_wins.items():
    key_pretty = re.sub('-autfilt-States', '', key)
    tab_wins.append([key_pretty,
                     df_summary.loc[key]["mean"],
                     df_summary.loc[key]["median"],
                     val['wins'],
                     # val['winsTO'],
                     val['losses'],
                     # val['lossesTO'],
                     df_summary.loc[key]["timeouts"],
                    ])
  headers_wins = ["method",
                  "mean",
                  "median",
                  "wins",
                  # "wins-timeouts",
                  "losses",
                  # "losses-timeouts",
                  "timeouts",
                 ]
  #table_to_file(tab_wins, headers_wins, out_prefix + "_table1right")
  print(tab.tabulate(tab_wins, headers=headers_wins, tablefmt="github"))
