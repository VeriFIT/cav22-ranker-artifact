#!/bin/bash

# Check the number of command-line arguments
if [ \( "$#" -lt 1 \) ] ; then
	echo "usage: ${0} <input-ba> [params]"
	exit 1
fi

BINDIR=$(dirname $(readlink -f $0))
SPOTEXE="${BINDIR}/autfilt"

INPUT=$1
shift
params="$*"

TMP=$(mktemp)
TMP_STAT=$(mktemp)
SPOTEXE=${SPOTEXE} ${BINDIR}/ranker --stats ${params} ${INPUT} > ${TMP} 2> ${TMP_STAT} || exit 1

set -o pipefail
autfilt_out=$(LD_LIBRARY_PATH=${BINDIR} ${SPOTEXE} --high ${TMP} | grep "^States:" | sed 's/^States/autfilt-States/')
ret=$?
rm ${TMP}

cat ${TMP_STAT} | sed 's/^Generated-states:/nopost-States:/' | sed 's/^Generated-trans:/nopost-Transitions:/'
echo ${autfilt_out}

rm ${TMP_STAT}

exit ${ret}
