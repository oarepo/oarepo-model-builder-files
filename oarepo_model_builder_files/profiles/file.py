from pathlib import Path
from typing import Union, List

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles import Profile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.dict import dict_get


class FileProfile(Profile):
    # schema - ideas - build new schema from specifications of the submodel??
    # but I still probably need some of the old settings in the new schema and this would overwrite them?

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        parent_record = model.get_schema_section("record", ["record"])
        builder.build(model, profile, model_path, output_directory, context={
            'parent_record': parent_record
        })
