from oarepo_model_builder_files.builders.base import BaseBuilder


class InvenioFilesResourceConfigBuilder(BaseBuilder):
    TYPE = "invenio_record_resource_config"
    section = "resource-config"
    template = "resource-config"