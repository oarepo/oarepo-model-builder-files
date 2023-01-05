import copy
import os
import re
from io import StringIO
from pathlib import Path
from typing import Dict

import pytest
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model, load_entry_points_dict
from oarepo_model_builder.fs import AbstractFileSystem


# from tests.mock_filesystem import MockFilesystem


class MockFilesystem(AbstractFileSystem):
    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def open(self, path: str, mode: str = "r"):
        path = Path(path).absolute()
        if mode == "r":
            if not path in self.files:
                raise FileNotFoundError(
                    f"File {path} not found. Known files {[f for f in self.files]}"
                )
            return StringIO(self.files[path].getvalue())
        self.files[path] = StringIO()
        self.files[path].close = lambda: None
        return self.files[path]

    def exists(self, path):
        path = Path(path).absolute()
        return path in self.files

    def mkdir(self, path):
        pass

    def snapshot(self):
        ret = {}
        for fname, io in self.files.items():
            ret[fname] = io.getvalue()
        return ret


def remove_whitespaces(str):
    return re.sub(r"\s", "", str)


def is_in(str1, str2):
    return remove_whitespaces(str1) in remove_whitespaces(str2)


def equals_sans_whitespaces(str1, str2):
    s1 = remove_whitespaces(str1)
    s2 = remove_whitespaces(str2)
    return s1 == s2


def update_dict(dct, k, *args):
    ret = copy.deepcopy(dct)
    new = {}
    for arg in args:
        new = new | arg
    ret[k] = new
    return ret

"""
SIMPLE = {"simple": {}}

CUSTOM_ACTION_NAME = {
    "custom-action-name": {"action-class-name": "ApproveMeGoddamnAction"}
}

CUSTOM_ACTION_CLASS = {
    "custom-action": {
        "action-class": "tests.requests_actions.ActuallyApproveRecordAction",
        "generate-action-class": False,
    }
}

CUSTOM_ACTION_BASE_CLASS = {
    "custom-action-base": {
        "action-class-bases": ["tests.requests_actions.ActuallyApproveRecordAction"]
    }
}

CUSTOM_TYPE_NAME = {"custom-type-name": {"type-class-name": "MyTypeCustomName"}}

CUSTOM_TYPE_CLASS = {
    "custom-type": {
        "type-class": "tests.requests_types.MyTypeCustomClass",
        "generate-type-class": False,
    }
}

CUSTOM_TYPE_BASE_CLASS = {
    "custom-type-base": {"type-class-bases": ["tests.requests_types.MyTypeCustomClass"]}
}
"""
MODEL_BASE = {
    "oarepo:use": "invenio",
    "model": {
        "properties": {
            "metadata": {
                "properties": {
                    "title": {"type": "fulltext+keyword"},
                    "status": {"type": "keyword"},
                }
            }
        }
    },
}

FILES_MODEL = {
    "oarepo:use": "invenio",
    "model": {
        "properties": {
            "metadata": {
                "properties": {
                    "title": {"type": "fulltext+keyword"},
                }
            }
        }
    },
 #   "settings": {
 #       "package": "test_file"
 #   }
}


"""
MODEL_ONE_REQUEST = update_dict(MODEL_BASE,
                                "requests",
                                APPROVE_REQUEST
                                )

MODEL_TWO_REQUESTS = update_dict(MODEL_BASE,
                                 "requests",
                                 APPROVE_REQUEST,
                                 PUBLISH_REQUEST,
                                 ACTUALLY_APPROVE_REQUEST,
                                 )

MODEL_ALL = update_dict(
    MODEL_BASE,
    "requests",
    SIMPLE,
    CUSTOM_ACTION_NAME,
    CUSTOM_ACTION_CLASS,
    CUSTOM_ACTION_BASE_CLASS,
    CUSTOM_TYPE_NAME,
    CUSTOM_TYPE_CLASS,
    CUSTOM_TYPE_BASE_CLASS,
)
"""


def generate_source(model):
    model["model"]["submodel"] = FILES_MODEL
    schema = load_model(
        "test.yaml",
        "test",
        model_content=model,
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    actions = builder.filesystem.open(
        os.path.join("test", "requests", "actions.py")
    ).read()
    resolvers = builder.filesystem.open(
        os.path.join("test", "requests", "resolvers.py")
    ).read()
    types = builder.filesystem.open(os.path.join("test", "requests", "types.py")).read()
    return actions, resolvers, types


def test_profiles():
    model = copy.deepcopy(MODEL_BASE)
    model["files"] = FILES_MODEL

    model = load_model(
        "test.yaml",
        "test",
        model_content=model,
        isort=False,
        black=False,
    )
    profile = 'model'
    profile2 = 'files'
    try:
        profile_handler = load_entry_points_dict("oarepo_model_builder.profiles")[
            profile
        ]()
        profile_handler_files = load_entry_points_dict("oarepo_model_builder.profiles")[
            profile2
        ]()
    except KeyError:
        raise AttributeError(f"No profile handler for {profile} registered")

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder_file = create_builder_from_entrypoints(profile="files", filesystem=filesystem)

    profile_handler.build(model, "", builder)
    profile_handler_files.build(model, "", builder_file)
    print()

def test_model_no_request():
    schema = load_model(
        "test.yaml",
        "test",
        model_content=MODEL_BASE,
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    with pytest.raises(FileNotFoundError):
        builder.filesystem.open(os.path.join("test", "requests", "actions.py")).read()
    with pytest.raises(FileNotFoundError):
        builder.filesystem.open(os.path.join("test", "requests", "resolvers.py")).read()
    with pytest.raises(FileNotFoundError):
        builder.filesystem.open(os.path.join("test", "requests", "types.py")).read()