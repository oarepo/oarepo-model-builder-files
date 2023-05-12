from oarepo_model_builder_files.builders.base import BaseBuilder


class InvenioFilesSchemaBuilder(BaseBuilder):
    TYPE = "invenio_files_schema"
    section = "marshmallow"
    template = "files-schema"
