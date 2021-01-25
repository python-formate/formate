# 3rd party
import pytest

# this package
from formate.classes import Hook
from formate.exceptions import HookNotFoundError
from formate.reformat_generics import reformat_generics
from formate.utils import import_entry_points, normalize


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
def test_normalize(value, expects):
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
