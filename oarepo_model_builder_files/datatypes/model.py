from oarepo_model_builder.datatypes import (
    DataTypeComponent,
    Section,
    ModelDataType,
    Import,
)
from oarepo_model_builder.datatypes.model import Link
from ..profiles.file import FileProfile


class ModelFilesComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    def process_links(self, datatype, section: Section, **kwargs):
        if not isinstance(datatype.profile, FileProfile):
            section.config["item"].append(
                Link(
                    name="files",
                    link_class="RecordLink",
                    link_args=['"{self.url_prefix}{id}/files"'],
                    imports=[
                        Import(
                            import_path="invenio_records_resources.services.RecordLink"
                        )
                    ],
                )
            )

    def process_mb_invenio_record_service_config(self, *, datatype, section, **kwargs):
        if isinstance(datatype.profile, FileProfile):
            # override class as it has to be a parent class
            section.config["record-class"] = datatype.definition["record-parent-class"]
