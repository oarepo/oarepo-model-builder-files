from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name

class InvenioFilesParentRecordBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_files_parent_record"
    template = "files-parent-record"

    def finish(self, **extra_kwargs):
        python_path = self.class_to_path(self.settings.parent_schema.settings.python.record_class)
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(self.settings.parent_schema.settings.python.record_class),
            parent_settings=self.settings.parent_schema.settings,
            **extra_kwargs,
        )