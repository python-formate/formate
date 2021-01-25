# this package
from formate.mini_hooks import ellipsis_reformat, noqa_reformat


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


def test_ellipsis_reformat():
	code = [
			"def foo():",
			"\t...",
			]
	expected = [
			"def foo(): ...",
			]

	assert ellipsis_reformat('\n'.join(code)) == '\n'.join(expected)

	assert ellipsis_reformat('\n'.join(expected)) == '\n'.join(expected)

	code = ["def foo() -> str:", "\t..."]
	expected = ["def foo() -> str: ..."]
	assert ellipsis_reformat('\n'.join(code)) == '\n'.join(expected)
