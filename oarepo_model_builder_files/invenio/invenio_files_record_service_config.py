from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name

class InvenioRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_files_record_service_config"
    class_config = "record-service-config-class"
    template = "files-service-config"

    def finish(self, **extra_kwargs):
        python_path = self.class_to_path(self.settings.python[self.class_config])
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(self.settings.python[self.class_config]),
            **extra_kwargs,
        )