from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class InvenioModelFilesAfterPreprocessor(ModelPreprocessor):
    TYPE = "invenio_files_after"

    def transform(self, schema, settings):
        files = schema.schema["files"]
        model = schema.schema["model"]

        files["record-search-options-class"] = ""
        files["schema-name"] = ""
        files["mapping-file"] = ""
