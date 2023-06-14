import re

import marshmallow as ma

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.utils.python_name import parent_module, base_name
from oarepo_model_builder.validation.utils import ImportSchema
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder.datatypes.components import RecordModelComponent


class FilesFieldSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Set to True (default) provider class"})
    field_class = ma.fields.String(
        attribute="field-class",
        data_key="field-class",
    )
    file_class = ma.fields.String(
        attribute="file-class",
        data_key="file-class",
    )
    field_args = ma.fields.List(
        ma.fields.String(),
        attribute="field-args",
        data_key="field-args",
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "A list of python imports"}
    )
    skip = ma.fields.Boolean()


class FilesFieldModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    depends_on = [RecordModelComponent]

    class ModelSchema(ma.Schema):
        files_field = ma.fields.Nested(
            FilesFieldSchema,
            attribute="files-field",
            data_key="files-field",
            metadata={"doc": "Files field settings"}
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record = datatype.definition["record"]


        files_field = set_default(datatype, "files-field", {})
        files_field.setdefault("generate", True)
        files_field.setdefault("field-class", "FilesField")
        files_field.setdefault("file-class", base_name(file_record["class"]))
        files_field.setdefault("field-args", ["store=False"])
        files_field.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.records.systemfields.FilesField"
                },
                {
                    "import": file_record["class"]
                },
            ],
        )
