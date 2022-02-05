# stdlib
import ast

# 3rd party
import pytest

# this package
from formate.classes import Hook
from formate.exceptions import HookNotFoundError
from formate.reformat_generics import reformat_generics
from formate.utils import import_entry_points, normalize, syntaxerror_for_file


@pytest.mark.parametrize(
		"value, expects",
		[
				("foo", "foo"),
				("Foo", "foo"),
				("FOO", "foo"),
				("foo-bar", "foo-bar"),
				("foo_bar", "foo-bar"),
				("foo-bar-baz", "foo-bar-baz"),
				("foo_bar_baz", "foo-bar-baz"),
				("foo_bar-baz", "foo-bar-baz"),
				]
		)
def test_normalize(value: str, expects: str):
	assert normalize(value) == expects


def test_import_entry_points():
	hooks = [Hook(
			name="reformat-generics",
			priority=40,
			)]

	entry_points = import_entry_points(hooks)
	assert entry_points
	assert len(entry_points) == 1

	assert list(entry_points.keys()) == ["reformat-generics"]
	assert entry_points["reformat-generics"].name == "reformat-generics"
	assert entry_points["reformat-generics"].obj == reformat_generics


def test_import_entry_points_not_found():
	hooks = [Hook(
			name="i-dont-exist",
			priority=40,
			)]

	with pytest.raises(HookNotFoundError, match="No such hook 'i-dont-exist'. Is it installed?") as e:
		import_entry_points(hooks)

	assert e.value.hook is hooks[0]


def test_syntaxerror_for_file():

	with pytest.raises(SyntaxError) as exc_info:  # noqa: PT012
		with syntaxerror_for_file("code.py"):
			ast.parse("def foo()pass")

	assert exc_info.value.filename == "code.py"

	with pytest.raises(SyntaxError) as exc_info:  # noqa: PT012
		with syntaxerror_for_file("__init__.py"):
			ast.parse("def foo()pass")

	assert exc_info.value.filename == "__init__.py"

	with pytest.raises(SyntaxError) as exc_info:  # noqa: PT012
		with syntaxerror_for_file("code.py"):
			ast.parse("def foo()pass", filename="code.py")

	assert exc_info.value.filename == "code.py"

	with pytest.raises(SyntaxError) as exc_info:  # noqa: PT012
		with syntaxerror_for_file("code.py"):
			ast.parse("def foo()pass", filename="__init__.py")

	assert exc_info.value.filename == "__init__.py"
