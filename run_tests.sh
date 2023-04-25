#!/bin/bash
set -e

MODEL="example"
VENV=".model_venv"
#export OPENSEARCH_PORT=9400

if test -d ./tests/$MODEL; then
	rm -rf ./tests/$MODEL
fi
oarepo-compile-model ./tests/$MODEL.yaml --output-directory ./tests/$MODEL --profile model,files -vvv
python3 -m venv $VENV
. $VENV/bin/activate
pip install -U setuptools pip wheel
pip install 'oarepo>=11.0.26,<12.0.0'
pip uninstall -y invenio_oauth2server
pip install "./tests/$MODEL[tests]"
pytest tests/$MODEL/tests