import marshmallow as ma
from oarepo_model_builder.datatypes import (
    DataType,
    DataTypeComponent,
    Import,
    ModelDataType,
    Section,
)
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    RecordMetadataModelComponent,
)
from oarepo_model_builder.datatypes.components.model.pid import process_pid_type
from oarepo_model_builder.datatypes.components.model.utils import (
    append_array,
    place_after,
    set_default,
)
from oarepo_model_builder.datatypes.model import Link


def get_file_schema():
    from ..file import FileDataType

    return FileDataType.validator()

class FileComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        files = ma.fields.Nested(get_file_schema)

    def process_links(self, datatype, section: Section, **kwargs):
        if self.is_record_profile:
            # add files link item
            has_files = False
            for link in section.config["links_item"]:
                if link.name == "files":
                    has_files = True
            if not has_files:
                section.config["links_item"].append(
                    Link(
                        name="files",
                        link_class="RecordLink",
                        link_args=['"{self.url_prefix}{id}/files"'],
                        imports=[
                            Import(
                                import_path="invenio_records_resources.services.RecordLink" # NOSONAR
                            )
                        ],
                    )
                )
        if self.is_file_profile:
            if "links_search" in section.config:
                section.config.pop("links_search")
            # remove normal links and add
            section.config["file_links_list"] = [
                Link(
                    name="self",
                    link_class="RecordLink",
                    link_args=['"{self.url_prefix}{id}/files"'],
                    imports=[Import("invenio_records_resources.services.RecordLink")],
                ),
            ]

            section.config.pop("links_item")
            section.config["file_links_item"] = [
                Link(
                    name="self",
                    link_class="FileLink",
                    link_args=['"{self.url_prefix}{id}/files/{key}"'],
                    imports=[Import("invenio_records_resources.services.FileLink")], # NOSONAR
                ),
                Link(
                    name="content",
                    link_class="FileLink",
                    link_args=['"{self.url_prefix}{id}/files/{key}/content"'],
                    imports=[Import("invenio_records_resources.services.FileLink")],
                ),
                Link(
                    name="commit",
                    link_class="FileLink",
                    link_args=['"{self.url_prefix}{id}/files/{key}/commit"'],
                    imports=[Import("invenio_records_resources.services.FileLink")],
                ),
            ]

    def process_mb_invenio_record_service_config(self, *, datatype, section, **kwargs):
        if self.is_file_profile:
            # override class as it has to be a parent class
            section.config.setdefault("record", {})[
                "class"
            ] = datatype.parent_record.definition["record"]["class"]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        self.is_record_profile = context["profile"] == "record"
        self.is_file_profile = context["profile"] == "files"
        if not self.is_file_profile:
            return

        parent_record_datatype: DataType = context["parent_record"]
        datatype.parent_record = parent_record_datatype

        permissions = set_default(datatype, "permissions", {})
        permissions.setdefault(
            "class", parent_record_datatype.definition["permissions"]["class"]
        )
        permissions.setdefault("generate", False)


        pid = set_default(datatype, "pid", {})
        pid.setdefault(
            "type",
            process_pid_type(parent_record_datatype.definition["pid"]["type"] + "File"),
        )


        set_default(datatype, "search-options", {}).setdefault("skip", True)
        set_default(datatype, "json-schema-settings", {}).setdefault("skip", True)
        set_default(datatype, "mapping-settings", {}).setdefault("skip", True)
        set_default(datatype, "record-dumper", {}).setdefault("skip", True)

"""
class FileMetadataComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [RecordMetadataModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if context["profile"] != "files":
            return

        place_after(
            datatype,
            "record-metadata",
            "base-classes",
            "RecordMetadataBase",
            "FileRecordModelMixin",
        )
        append_array(
            datatype,
            "record-metadata",
            "imports",
            {"import": "invenio_records_resources.records.FileRecordModelMixin"},
        )
"""