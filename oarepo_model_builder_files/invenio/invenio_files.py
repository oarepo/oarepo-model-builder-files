from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
from oarepo_model_builder.utils.jinja import package_name

class InvenioFilesClassPythonBuilder(InvenioBaseClassPythonBuilder):
    MODULE = None

    def get_module(self):
        return package_name(self.model[self.class_config])

    def finish(self, **extra_kwargs):
        module = self.MODULE if self.MODULE else self.get_module()
        python_path = self.module_to_path(module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=module,
            files=self.schema.files,
            model=self.schema.model,
            **extra_kwargs,
        )

    def process_template(self, python_path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = HyphenMunch(settings=self.settings, **extra_kwargs)
        template = self.call_components(
            "invenio_before_python_template", template, context=context
        )
        output.merge(template, context)
