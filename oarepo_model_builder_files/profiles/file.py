import copy
from pathlib import Path
from typing import Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.conflict_resolvers import AutomaticResolver
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.profiles import Profile

from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
import munch


class FileProfile(Profile):
    # schema - ideas - build new schema from specifications of the submodel??
    # but I still probably need some of the old settings in the new schema and this would overwrite them?
    #
    # required_profiles = ('model',)
    def build(
            self,
            model: ModelSchema,
            output_directory: Union[str, Path],
            builder: ModelBuilder,
    ):
        # todo how the settings for the file model should look like exactly?
        # todo how the schema for defining the file model (or submodels in general) should look like? Should there be a
        # specific schema for types of models to prevent recursion for specific types for example?
        # new_model = copy.deepcopy(model)
        parent_model_builder = create_builder_from_entrypoints(
            profile='model', conflict_resolver=AutomaticResolver(resolution_type="replace"), overwrite=True
        )
        parent_model_builder.set_schema(model)
        parent_model_builder._run_model_preprocessors(model)

        new_schema = model.schema["files"]
        # todo - perhaps use load_model from entrypoints
        new_model = ModelSchema(file_path=model.file_path, content=new_schema, included_models=model.included_schemas,
                                loaders=model.loaders)
        #---- quick fix

        #----

        new_model.schema.settings["package"] = model.schema.settings.package


        new_model.schema.settings.python = HyphenMunch()
        python = new_model.schema.settings.python
        new_model.schema.settings["parent-schema"] = model.schema

        python.use_isort = model.schema.settings.python.use_isort
        python.use_black = model.schema.settings.python.use_black


        """
        #api
        
        new_python.setdefault("record-bases", ["invenio_records_resources.records.api.FileRecord"])

        #models
        
        new_python.setdefault("record-metadata-bases", ["invenio_records_resources.records.FileRecordModelMixin"])

        #resource
        new_python.setdefault("record-resource-class-bases", ["invenio_records_resources.resources.files.resource.FileResource"])

        #resource config
        new_model.schema.settings["collection-url"] = f'{model.schema.settings["collection-url"]}<pid_value>'
        new_python.setdefault("record-resource-config-class-bases",
                              ["invenio_records_resources.resources.FileResourceConfig"])

        #service config

        new_python.setdefault("record-service-config-components", [])
        new_python.setdefault("record-service-config-bases", ["invenio_records_resources.services.FileServiceConfig"])
        
        new_python.setdefault("record-permissions-class", old_python.record_permissions_class)
        new_python.setdefault("parent-service-id",old_python.flask_extension_name)
        new_python.setdefault("service-id", f"{old_python.service_id}_file")

        #service
        new_python.setdefault("record-service-bases", ["invenio_records_resources.services.FileService"])

        #views and ext
        new_python.setdefault("init-indexer", False) #indexer is not defined for FileService
        new_python.setdefault("create-blueprint-from-app", f"{old_python.create_blueprint_from_app}_files")
        new_python.setdefault("config-resource-register-blueprint-key", f"{old_python.config_resource_register_blueprint_key}_FILES")
        new_python.setdefault("config-service-class-key", f"{old_python.config_service_class_key}_FILES")
        new_python.setdefault("config-service-config-key", f"{old_python.config_service_config_key}_FILES")
        new_python.setdefault("config-resource-class-key", f"{old_python.config_resource_class_key}_FILES")
        new_python.setdefault("config-resource-config-key", f"{old_python.config_resource_config_key}_FILES")
        new_python.setdefault("flask-extension-name", f"{old_python.flask_extension_name}_files") # todo what about the proxy?

        #tests
        # todo
        new_model.schema.settings["parent-collection-url"] = model.schema.settings["collection-url"]

        #### todo temporary solution
        new_python.use_isort = model.schema.settings.python.use_isort
        new_python.use_black = model.schema.settings.python.use_black

        #enabled files field
        new_model.schema.model.properties.files = HyphenMunch()
        new_model.schema.model.properties.files.properties = HyphenMunch()
        new_model.schema.model.properties.files.properties.enabled = HyphenMunch()
        new_model.schema.model.properties.files.properties.enabled["type"] = "boolean"
        new_model.schema.model.properties.files["oarepo:marshmallow"] = HyphenMunch()
        new_model.schema.model.properties.files["oarepo:marshmallow"]["generate"] = True
        new_model.schema.model.properties.files["oarepo:marshmallow"]["class"] = f"{model.schema.settings['package']}.services.schema.FilesOptionsSchema"
        """
        """
        settings = new_model.settings.python
        
        def edit_base_name(str, new_base):
            return f"{str.rsplit('.', 1)[0]}.{new_base}"

        settings["record-class"] = edit_base_name(settings["record-class"], "TestFileRecord")

        
        new_settings = {}
        new_settings["package"] = "testfile"
        new_settings = munch.munchify(new_settings, factory=HyphenMunch)
        new_settings["python"] = HyphenMunch()

        #new_model.settings = new_settings
        new_model.schema.settings = new_settings
        """
        builder.build(new_model, output_directory)