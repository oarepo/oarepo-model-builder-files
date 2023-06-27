#!/bin/bash
set -e

BUILDER_VENV=.venv
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -e .

VENV=".model_venv"

if test -d example-model; then
	rm -rf example-model
fi
if test -d $VENV ; then
	rm -rf $VENV
fi

oarepo-compile-model ./tests/example.yaml --output-directory ./tests/example-model --profile record,files -vvv
python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel
pip install "./tests/example-model[tests]"
pytest tests/example-model/tests