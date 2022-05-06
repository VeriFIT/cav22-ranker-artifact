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

3. Smoke test (~20 mins)
========================

To run the smoke test (check whether everything is setup in the correct way),
perform the following sequence:

  a) Change directory to the evaluation environment

     $ cd ~/cav22-ranker-artifact/ba-compl-eval

  b) Run the smoke tests (the smoke tests run each tool on one chosen automaton
     from each set; the chosen automaton should be easy and should not cause
     timeout or other problems):

     $ ./run_minimal_automizer-smoke.sh
     $ ./run_minimal_ltl-smoke.sh
     $ ./run_minimal_random-smoke.sh
     $ ./run_other_automizer-smoke.sh
     $ ./run_other_ltl-smoke.sh
     $ ./run_other_random-smoke.sh

     There should not be any failures.  If there are, you can try to check the
     produced *.tasks files for error messages.

  c) Collect the results

     $ ./collect_results.sh

     This command merges files for the 'minimal' and 'other' set of tools for
     each benchmark and produce CSV files in the eval/ directory that will be
     used to generate plots and tables in the following step.

  d) Produce the plots and tables for the smoke test

     $ cd eval
     $ ./gen_results.py | tee results.txt

     Again, this should go through smoothly.  The following files will be
     created in the eval/ directory:

       * fig_ranker-nopost_vs_ranker-iw-orig-nopost.pdf         -- Fig. 3a
       * fig_ranker-nopost_vs_ranker-sd-ncsb-lazy-nopost.pdf    -- Fig. 3b
       * fig_ranker-autfilt_vs_ranker-tacas22-autfilt.pdf       -- Fig. 4a
       * fig_ranker-autfilt_vs_spot-autfilt.pdf                 -- Fig. 4b
       * results.txt                                            -- Tables 1--3

     In the smoke test, the plots in the pdf files will be populated by very
     little data points (possibly zero) and the tables in results.txt will not
     contain many values (sometimes there will even be nan).  This is expected.
     You can view the pdf files e.g. using evince, e.g.,

       $ evince fig_ranker-nopost_vs_ranker-iw-orig-nopost.pdf

  e) If you have come this far, congratulations, the smoke test has been
     successful.

4. Replication of results for Ranker and Spot (< 1 day)
=======================================================
This step replicates the results for various versions of Ranker and Spot, and
obtains the following outputs:

  * Fig. 3a,b
  * Fig. 4a,b
  * Table 1
  * Table 2, rows Ranker, RankerOld (denoted as ranker-tacas22), Spot
  * Table 3, rows Ranker, RankerOld (denoted as ranker-tacas22), Spot

Some notes about running the experiments:

  * In order to get the results in reasonable time, we decreased the timeout
    from 300 s (used for the data in the paper) to 60 s.  You can set the
    timeout back to 300 s by changing the value of the TIMEOUT variable in
    scripts/run_experiments.sh .

  * By default, the benchmarking program will run the experiments sequentially.
    If you wish to run the experiments in parallel (note that this might cause
    issues, e.g., by various processes stealing the available memory, causing
    some out-of-memory results), you can modify the value of the JOBS variable
    in scripts/run_experiments.sh .

  * The benchmarking program prinouts out the progress of the benchmark (e.g.
    1234/4567) and results of the tests, which are usually FINISHED, TIMEOUT,
    or ERROR.  The ERROR is usually caused by out-of-memory (or by some other
    issue for other tools, such as stack overflow for ROLL), so don't worry if
    you see it, it is expected and is processed as "timeout" in the evaluation.
    Detailed outputs are written into *.tasks files, which are later
    transformed into CSV tables.

  * You can terminate the benchmarking program at any point by pressing CTRL-C
    (possibly multiple times to kill all threads).  The output *.tasks file can
    be used as if the benchmark finished successfully (the missing results
    might be reported as "timeouts").  Using this, you can get partial results
    if you do not have the time/resources to run all experiments.

The replication is performed by the following sequence of steps:

  a) Change directory to the evaluation environment

     $ cd ~/cav22-ranker-artifact/ba-compl-eval

  b) Run the smoke tests for other tools than Ranker and Spot:

     $ ./run_other_automizer-smoke.sh
     $ ./run_other_ltl-smoke.sh
     $ ./run_other_random-smoke.sh

     This makes sure that the results processing scripts do not fail because of
     some missing columns.

  c) Run the tests for Ranker and Spot.  Warning: this may take a long time
     (each test from 30 mins to several hours, the fastest one is the LTL, so
     you can let that one go through; for the rest (Automizer, random), if you
     do not have the time, kill them at some point (e.g. after one hour) and
     use the so-far computed data).

     $ ./run_minimal_ltl.sh
     $ ./run_minimal_automizer.sh
     $ ./run_minimal_random.sh

  c) Collect the results

     $ ./collect_results.sh

  d) Produce the plots and tables

     $ cd eval
     $ ./gen_results.py | tee results.txt

     The plots are in the fig*.pdf files and the tables are in results.txt



