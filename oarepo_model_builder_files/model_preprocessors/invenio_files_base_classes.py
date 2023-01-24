from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case

class InvenioModelFilesBaseClassesPreprocessor(ModelPreprocessor):
    TYPE = "invenio_files_base_classes"

    def transform(self, schema, settings):
        self.set_default_and_append_if_not_present(schema.model, "record-resource-class-bases", [],
                                                   "invenio_records_resources.resources.files.resource.FileResource")
        self.set_default_and_append_if_not_present(schema.model, "record-resource-config-class-bases", [],
                                                   "invenio_records_resources.resources.FileResourceConfig")
        self.set_default_and_append_if_not_present(schema.model, "record-service-bases", [],
                                                   "invenio_records_resources.services.FileService")
        self.set_default_and_append_if_not_present(schema.model, "record-bases", [],
                                                   "invenio_records_resources.records.api.FileRecord")
        self.set_default_and_append_if_not_present(schema.model, "record-service-config-bases", [],
                                                   "invenio_records_resources.services.FileServiceConfig")
        self.set_default_and_append_if_not_present(schema.model, "record-metadata-bases", [],
                                                   "invenio_records_resources.records.FileRecordModelMixin")
        #schema.model.marshmallow["schema-class"]