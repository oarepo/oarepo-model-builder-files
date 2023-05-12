#!/bin/bash
set -e

VENV=".model_venv"
#export OPENSEARCH_PORT=9400
#cd $(dirname $0)/..
if test -d example-model; then
	rm -rf example-model
fi
if test -d $VENV ; then
	rm -rf $VENV
fi

oarepo-compile-model ./tests/example.yaml --output-directory ./example-model --profile record,files -vvv
python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel
pip install "./example-model[tests]"
pytest example-model/tests