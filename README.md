Artifact for the CAV'22 submission "Complementing Büchi automata with Ranker" (VM version)
==========================================================================================
This file describes the provided virtual machine (VM) image containing the
artifact for the CAV'22 submission named "Complementing Büchi automata with
Ranker".  See README-pkg.md for a description of the "package" version of the
artifact, i.e., a version that only contains the tool and evaluation
environment, without the operating system (we provide the package version in
order to allow easier reuse of the tool and the evaluation environment by other
researchers).

The artifact reproduces the results from the paper, i.e., it runs several tool
for complementation of Büchi automata and compares the results (sizes of the
complements and the runtimes).

1. Requirements
===============

The VM was tested on a VM with 4 GiB of RAM and 1 CPU core at 2.30 GHz.
Providing more RAM may help obtain less out-of-memory failures (which we
categorize as "timeouts").  Providing more cores may be counterproductive; by
default, the evaluation will run one task on each available core, which might
cause interference, in particular wrt. memory (cf. details below).

2. Structure
============

~/cav22-ranker-artifact/
├── ba-compl-eval/          -- the evaluation environment
│   ├── automata/           -- repository of automata
│   ├── bench/              -- code for running experiments
│   ├── bin/                -- tools and wrappers
│   ├── eval/               -- code for generating plots and tables
│   ├── ref_outputs/        -- reference outputs for results presented in the paper
│   ├── scripts/            -- auxiliary scripts for evaluation
│   ├── util/               -- some helpful scripts (not needed for the evaluation)
│   ├── collect_results.sh  -- collects results for plot and table generation
│   └── run-*.sh            -- runs some subset of experiments (described below)
├── pkgs/               -- source code of the tools
│   └── ranker/         -- source code of Ranker
├── LICENSE             -- the license
├── README.md           -- this file
└── README-pkg.md       -- README for the package version

3. Smoke test (~45 mins)
========================

To run the smoke test (check whether everything is setup in the correct way),
perform the following sequence:

  1) change directory to the evaluation environment

     $ cd ~/cav22-ranker-artifact/ba-compl-eval

  2) run each test for ~6 mins (for the smoke test, it is enough for each tool
     to finish successfully on at least one automaton, in order not to break the
     table and plot generation scripts)

     $ ./run_minimal_automizer.sh
     $ ./run_minimal_ltl.sh
     $ ./run_minimal_random.sh
     $ ./run_other_automizer.sh
     $ ./run_other_ltl.sh
     $ ./run_other_random.sh






3. Replication of results
=========================

TODO
