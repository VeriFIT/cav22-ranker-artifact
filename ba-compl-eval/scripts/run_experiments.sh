#!/bin/bash

# Check the number of command-line arguments
if [ \( "$#" -lt 2 \) ] ; then
	echo "This script will run all experiments from <input-set>, including the tools that are not"
	echo "in the graphs in the paper (expect long running time!!), unless set otherwise in [methods]"
	echo
	echo "usage: ${0} <input-set> <output-file> [methods]"
	echo
	echo "   with <input-set> in { ltl, random, automizer }"
	echo "   and [methods] being a semicolon-delimited list of methods (see bench/ba-compl.yaml)"
	exit 1
fi

INPUT="$1"
OUTPUT="$2"

METHODS=""
if [ \( "$#" -eq 3 \) ] ; then
	METHODS="-m $3"
fi

# timeout in seconds
TIMEOUT=60

# number of jobs
JOBS=1

BIN_DIR="$(pwd)/bin"
INPUT_FILE="${INPUT}.input"
TASK_FILE="../${OUTPUT}-to${TIMEOUT}.tasks"

export LD_LIBRARY_PATH="${BIN_DIR}"

cd bench
cat ${INPUT_FILE} | ./pycobench -t ${TIMEOUT} -j ${JOBS} ${METHODS} -o ${TASK_FILE} ba-compl.yaml
