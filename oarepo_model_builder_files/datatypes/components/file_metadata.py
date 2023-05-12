from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import (
    append_array,
    prepend_array,
)


class FileMetadataComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if context["profile"] == "file":
            return
        prepend_array(datatype, "record-metadata", "base-classes", "RecordMetadataBase")
        prepend_array(
            datatype, "record-metadata", "base-classes", "FileRecordModelMixin"
        )
        prepend_array(datatype, "record-metadata", "base-classes", "db.Model")
        append_array(
            datatype,
            "record-metadata",
            "imports",
            {"import": "invenio_records_resources.records.FileRecordModelMixin"},
        )
        append_array(
            datatype,
            "record-metadata",
            "imports",
            {"import": "invenio_db.db"},
        )
        append_array(
            datatype,
            "record-metadata",
            "imports",
            {"import": "invenio_records.models.RecordMetadataBase"},
        )
