black oarepo_model_builder_files tests --target-version py310
autoflake --in-place --remove-all-unused-imports --recursive oarepo_model_builder_files tests
isort oarepo_model_builder_files tests  --profile black
