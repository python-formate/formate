# stdlib
import re

# 3rd party
import pytest

# this package
from formate.classes import EntryPoint, Hook


def test_entrypoint_errors():

	with pytest.raises(
			TypeError,
			match=re.escape("Entry points must be callables (e.g. classes and functions), not <class 'str'>."),
			):
		EntryPoint(name="foo-bar", obj="not-a-callable")  # type: ignore


def test_hook_errors():
	hook: Hook = Hook(name="foo-bar")

	with pytest.raises(
			TypeError,
			match=re.escape("hook 'foo-bar' has no entry point configured."),
			):
		hook("print('hello world')", "<stdin>")
