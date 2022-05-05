#!/bin/bash

# Check the number of command-line arguments
if [ \( "$#" -ne 1 \) ] ; then
	echo "This script will run all experiments from <input-set> on the minimal tool set"
	echo
	echo "usage: ${0} <input-set>"
	echo
	echo "   with <input-set> in { ltl, random, automizer }"
	exit 1
fi

INPUT=$1

scripts/run_experiments.sh ${INPUT} 'spot;ranker;ranker-tacas22;ranker-iw-orig;ranker-sd-ncsb-lazy'
