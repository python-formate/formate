# stdlib
import os
import re

# 3rd party
from domdf_python_tools.compat import importlib_metadata


def test_click_version_against_tox():
	m = re.match(r"py.*-click(\d)\.(\d)", os.getenv("TOX_ENV_NAME", ''))
	if m is not None:
		target_version = tuple(map(int, m.groups()))
		click_version = tuple(map(int, importlib_metadata.version("click").split('.')[:2]))
		assert target_version == click_version
