# 3rd party
import pytest

# this package
from formate.mini_hooks import check_ast, noqa_reformat


def test_noqa_reformat():
	code = [
			"def foo():",
			'\t"""',
			"\tDoes something,",
			'\t"""',
			'',
			"  # noqa: D400  ",
			]
	expected = [
			"def foo():",
			'\t"""',
			"\tDoes something,",
			'\t"""  # noqa: D400  ',
			]
	assert noqa_reformat('\n'.join(code)) == '\n'.join(expected)

	assert noqa_reformat('\n'.join(expected)) == '\n'.join(expected)


def test_check_ast():
	code = [
			"def foo(:",
			'\t"""',
			"\tDoes something,",
			'\t"""',
			'',
			"  # noqa: D400  ",
			]

	with pytest.raises(SyntaxError):
		check_ast('\n'.join(code))

	code = [
			"def foo():",
			'"""',
			"\tDoes something,",
			'\t"""',
			'',
			"  # noqa: D400  ",
			]

	with pytest.raises(SyntaxError):
		check_ast('\n'.join(code))

	code = [
			"def foo():",
			'\t"""',
			"\tDoes something,",
			'\t"""',
			'',
			"  # noqa: D400  ",
			]

	assert check_ast('\n'.join(code)) == '\n'.join(code)
