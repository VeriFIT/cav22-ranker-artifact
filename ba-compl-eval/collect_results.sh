#!/bin/bash
MINIMAL="minimal-to60.tasks"
OTHER="other-to60.tasks"
cat automizer-${MINIMAL} automizer-${OTHER} > automizer-to60.tasks
cat ltl-${MINIMAL} ltl-${OTHER} > ltl-to60.tasks
cat random-${MINIMAL} random-${OTHER} > random-to60.tasks

bench/proc_results.py --csv automizer-to60.tasks > eval/automizer-to60.csv
bench/proc_results.py --csv ltl-to60.tasks > eval/ltl-to60.csv
bench/proc_results.py --csv random-to60.tasks > eval/random-to60.csv
