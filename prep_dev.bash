#!/bin/bash
# This is mainly here so I remember the pip install command.
PYVER=$(python --version)
if [[ ! $PYVER =~ 3\.[0-9]+.[0-9]+ ]]
    then
    echo "Bad python version. Must be 3, was: $PYVER" >&2
    exit 1
fi
PIPVER=$(pip --version)
if [[ ! $PIPVER =~ python3 ]]
    then
    echo "Bad pip version. Must be for python3, was: $PIPVER" >&2
    exit 1
fi

pip install -e .[develop]
rc=$?
if (( rc ))
    then
    echo $'\033[41m'"Error running pip install: $rc"$'\033[0m'
fi
