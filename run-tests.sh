#!/bin/bash
set -e

OAREPO_VERSION=${OAREPO_VERSION:-12}
BUILDER_VENV=".venv-builder"
VENV_TESTS=".venv-tests"
export PIP_EXTRA_INDEX_URL=https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple
export UV_EXTRA_INDEX_URL=https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple

if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

if test -d $VENV_TESTS ; then
	rm -rf $VENV_TESTS
fi


python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -e .

if test -d tests/example-model; then
	rm -rf tests/example-model
fi
oarepo-compile-model ./tests/example.yaml --output-directory ./tests/example-model --profile record,files -vvv

python3 -m venv $VENV_TESTS
. $VENV_TESTS/bin/activate
pip install -U setuptools pip wheel
pip install "oarepo[tests, rdm]==${OAREPO_VERSION}.*"
pip install "./tests/example-model[tests]"
pytest tests/example-model/tests

# model without files section should compile and run as well if omb is called in a virtualenv with files plugin

if test -d tests/example-model-no-files ; then
	rm -rf tests/example-model-no-files
fi
if test -d $VENV_TESTS ; then
	rm -rf $VENV_TESTS
fi

. $BUILDER_VENV/bin/activate

oarepo-compile-model ./tests/example_no_files.yaml --output-directory ./tests/example-model-no-files --profile record -vvv
python3 -m venv $VENV_TESTS
. $VENV_TESTS/bin/activate
pip install -U setuptools pip wheel
pip install "oarepo[tests, rdm]==${OAREPO_VERSION}.*"
pip install "./tests/example-model-no-files[tests]"
pytest tests/example-model-no-files/tests