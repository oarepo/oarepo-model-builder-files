from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder

class InvenioFilesRecordMetadataBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_files_record_metadata"
    class_config = "record-metadata-class"
    template = "files-record-metadata"