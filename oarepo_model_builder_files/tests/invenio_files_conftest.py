from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name

class InvenioFilesConftestBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_files_conftest"
    template = "files-conftest"
    MODULE = "tests.files.conftest"

    def finish(self, **extra_kwargs):
        python_path = self.module_to_path(self.MODULE)
        self.process_template(
            python_path,
            self.template,
            **extra_kwargs,
        )