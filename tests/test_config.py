# this package
from formate.classes import Hook
from formate.config import parse_global_config, parse_hooks
from formate.ellipses import ellipsis_reformat
from formate.imports import rewrite_collections_abc_imports


def test_parse_hooks():
	isort_kwargs = {
			"indent": "\t\t",
			"multi_line_output": 8,
			"import_heading_stdlib": "stdlib",
			}

	global_config = {"indent": '\t', "line_length": 115}

	config = {
			"hooks": {
					"reformat-generics": 40,
					"collections-import-rewrite": 20,
					"noqa-reformat": 60,
					"ellipsis-reformat": 70,
					"isort": {"priority": 50, "kwargs": isort_kwargs},
					},
			"config": global_config,
			}

	hooks = parse_hooks(config)

	assert isinstance(hooks[0], Hook)

	assert hooks[0].name == "collections-import-rewrite"
	assert hooks[0].priority == 20
	assert hooks[0].args == ()
	assert hooks[0].kwargs == {}
	assert hooks[0].entry_point is not None
	assert hooks[0].entry_point.obj is rewrite_collections_abc_imports
	assert hooks[0].global_config == global_config
	assert hooks[0].global_config is hooks[1].global_config

	assert hooks[2].name == "isort"
	assert hooks[2].kwargs == isort_kwargs
	assert hooks[2].kwargs is isort_kwargs

	assert len(hooks) == 5

	assert hooks[4].name == "ellipsis-reformat"
	assert hooks[4].entry_point is not None
	assert hooks[4].entry_point.obj is ellipsis_reformat


def test_parse_global_config():
	global_config = {"indent": '\t', "line_length": 115}

	assert parse_global_config({"config": global_config}) == global_config
