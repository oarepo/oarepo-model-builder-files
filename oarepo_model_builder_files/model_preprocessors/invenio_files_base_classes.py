from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case

class InvenioModelFilesBaseClassesPreprocessor(ModelPreprocessor):
    TYPE = "invenio_files_base_classes"

    def transform(self, schema, settings):
        python = settings.python
        python.setdefault("record-resource-class-bases", []).append(
            "invenio_records_resources.resources.files.resource.FileResource")
        python.setdefault("record-resource-config-class-bases", []).append("invenio_records_resources.resources.FileResourceConfig")
        python.setdefault("record-service-bases", []).append(
            "invenio_records_resources.services.FileService")
        python.setdefault("record-bases", []).append(
            "invenio_records_resources.records.api.FileRecord")
        python.setdefault("record-service-config-bases", []).append(
            "invenio_records_resources.services.FileServiceConfig")
        python.setdefault("record-metadata-bases", []).append(
            "invenio_records_resources.records.FileRecordModelMixin"
        )

        #todo - get it somewhere else
        python["record-search-options-class"] = ""