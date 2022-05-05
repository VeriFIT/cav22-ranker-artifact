#!/bin/bash

# Check the number of command-line arguments
if [ \( "$#" -lt 1 \) ] ; then
	echo "This script will run all experiments from <input-set>, including the tools that are not"
	echo "in the graphs in the paper (expect long running time!!), unless set otherwise in [methods]"
	echo
	echo "usage: ${0} <input-set> [methods]"
	echo
	echo "   with <input-set> in {from_ltl_red, advanced-automata, random-all-compact}"
	echo "   and [methods] being a semicolon-delimited list of methods (see bench/ba-compl.yaml)"
	exit 1
fi

INPUT="$1"

METHODS=""
if [ \( "$#" -eq 2 \) ] ; then
	METHODS="-m $2"
fi

# timeout in seconds
TIMEOUT=60

BIN_DIR="$(pwd)/bin"
INPUT_FILE="${INPUT}.input"
TASK_FILE="../${INPUT}-to${TIMEOUT}.tasks"

export LD_LIBRARY_PATH="${BIN_DIR}"

cd bench
cat from_ltl_red.input | ./pycobench -t ${TIMEOUT} ${METHODS} -o ${TASK_FILE} ba-compl.yaml
