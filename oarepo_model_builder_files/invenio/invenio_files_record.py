from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name

class InvenioFilesRecordBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_files_record"
    class_config = "record-class"
    template = "files-record"

    def finish(self, **extra_kwargs):
        print("I'M BUILDIIIING")
        python_path = self.class_to_path(self.settings.python[self.class_config])
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(self.settings.python[self.class_config]),
            **extra_kwargs,
        )