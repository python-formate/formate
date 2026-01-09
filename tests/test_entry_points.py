# 3rd party
import entrypoints  # type: ignore[import-untyped]
from coincidence import AdvancedDataRegressionFixture

# These tests will fail if not installed and just running straight from source


def test_entry_points():
	entry_points = entrypoints.get_group_all("formate_hooks")

	print(entry_points)

	hook_names = {e.name for e in entry_points}

	if "black" in hook_names:
		hook_names.remove("black")

	assert hook_names == {
		"reformat-generics",
		"dynamic_quotes",
		"noqa_reformat",
		"squish_stubs",
		"ellipsis_reformat",
		"collections-import-rewrite",
		"isort",
		"yapf",
	}, hook_names


def test_entry_points_file(advanced_data_regression: AdvancedDataRegressionFixture):
	for config, distro in entrypoints.iter_files_distros():
		if distro is not None and distro.name == "formate":
			advanced_data_regression.check(dict(config["formate_hooks"]))
			return

	raise ValueError("Not found")
