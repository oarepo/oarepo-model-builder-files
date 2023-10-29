#!/bin/bash
set -e

OAREPO_VERSION=${OAREPO_VERSION:-11}
OAREPO_VERSION_MAX=$((OAREPO_VERSION+1))

BUILDER_VENV=venv
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -e .

VENV=".model_venv"

if test -d tests/example-model; then
	rm -rf tests/example-model
fi
if test -d $VENV ; then
	rm -rf $VENV
fi

oarepo-compile-model ./tests/example.yaml --output-directory ./tests/example-model --profile record,files -vvv
python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install "./tests/example-model[tests]"
pytest tests/example-model/tests

# model without files section should compile and run as well if omb is called in a virtualenv with files plugin

if test -d tests/example-model-no-files ; then
	rm -rf tests/example-model-no-files
fi
if test -d $VENV ; then
	rm -rf $VENV
fi

. $BUILDER_VENV/bin/activate

oarepo-compile-model ./tests/example_no_files.yaml --output-directory ./tests/example-model-no-files --profile record -vvv
python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install "./tests/example-model-no-files[tests]"
pytest tests/example-model-no-files/tests