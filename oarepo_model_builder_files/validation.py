import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.validation.extensibility import ExtensibleSchema
from oarepo_model_builder.datatypes.model import ModelDataType


class FilesExtraSchema(ma.Schema):
    record_resource_parent_class = ma.fields.String(
        attribute="record-resource-parent-class",
        data_key="record-resource-parent-class",
    )
    record_resource_config_parent_class = ma.fields.String(
        attribute="record-resource-config-parent-class",
        data_key="record-resource-config-parent-class",
    )
    record_parent_class = ma.fields.String(
        attribute="record-parent-class", data_key="record-parent-class"
    )
    record_service_config_parent_class = ma.fields.String(
        attribute="record-service-config-parent-class",
        data_key="record-service-config-parent-class",
    )
    record_service_parent_class = ma.fields.String(
        attribute="record-service-parent-class", data_key="record-service-parent-class"
    )


class ModelFileExtraSchema(ma.Schema):
    files = fields.Nested(ExtensibleSchema("files", ModelDataType.validator))
