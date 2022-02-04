# 3rd party
import pytest

# this package
from formate.dynamic_quotes import dynamic_quotes

value_1 = """\
status_codes: Dict[str, str] = {
		"add": "A",
		"delete": "D",
		"modify": "M",
		}
"""

expected_1 = """\
status_codes: Dict[str, str] = {
		"add": 'A',
		"delete": 'D',
		"modify": 'M',
		}
"""

value_2 = """\
def foo():
	'''hello'''
"""


@pytest.mark.parametrize(
		"value, expects",
		[
				("'hello world'", '"hello world"'),
				("''", "''"),
				('""', "''"),
				("'a'", "'a'"),
				('"a"', "'a'"),
				("'Z'", "'Z'"),
				('"Z"', "'Z'"),
				("'5'", "'5'"),
				('"5"', "'5'"),
				("'☃'", "'☃'"),
				("'user'", '"user"'),
				('"☃"', "'☃'"),
				('print(123)\n"☃"', "print(123)\n'☃'"),
				('"☃"\nprint(123)', "'☃'\nprint(123)"),
				("'hello\\nworld'", "'hello\\nworld'"),
				('"hello\\nworld"', '"hello\\nworld"'),
				('"\\""', "'\"'"),
				('"quote \\""', "'quote \"'"),
				("'\\''", "\"'\""),
				("'quote \\''", "\"quote '\""),
				(value_1, expected_1),
				(value_2, value_2),
				('assert t.uname == "\\xe4\\xf6\\xfc"', 'assert t.uname == "äöü"'),
				('assert t.uname == "\\udce4\\udcf6\\udcfc"', 'assert t.uname == "\\udce4\\udcf6\\udcfc"'),
				]
		)
def test_quotes(value: str, expects: str):
	assert dynamic_quotes(value) == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				("def foo():\n\t'docstring'\n\t'hello world'", 'def foo():\n\t\'docstring\'\n\t"hello world"'),
				("def foo():\n\t'docstring'\n\t''", "def foo():\n\t'docstring'\n\t''"),
				('def foo():\n\t\'docstring\'\n\t""', "def foo():\n\t'docstring'\n\t''"),
				("def foo():\n\t'docstring'\n\t'a'", "def foo():\n\t'docstring'\n\t'a'"),
				('def foo():\n\t\'docstring\'\n\t"a"', "def foo():\n\t'docstring'\n\t'a'"),
				("def foo():\n\t'docstring'\n\t'Z'", "def foo():\n\t'docstring'\n\t'Z'"),
				('def foo():\n\t\'docstring\'\n\t"Z"', "def foo():\n\t'docstring'\n\t'Z'"),
				("def foo():\n\t'docstring'\n\t'5'", "def foo():\n\t'docstring'\n\t'5'"),
				('def foo():\n\t\'docstring\'\n\t"5"', "def foo():\n\t'docstring'\n\t'5'"),
				("def foo():\n\t'docstring'\n\t'☃'", "def foo():\n\t'docstring'\n\t'☃'"),
				("def foo():\n\t'docstring'\n\t'user'", 'def foo():\n\t\'docstring\'\n\t"user"'),
				('def foo():\n\t\'docstring\'\n\t"☃"', "def foo():\n\t'docstring'\n\t'☃'"),
				('def foo():\n\t\'docstring\'\n\tprint(123)\n"☃"', "def foo():\n\t'docstring'\n\tprint(123)\n'☃'"),
				('def foo():\n\t\'docstring\'\n\t"☃"\nprint(123)', "def foo():\n\t'docstring'\n\t'☃'\nprint(123)"),
				("def foo():\n\t'docstring'\n\t'hello\\nworld'", "def foo():\n\t'docstring'\n\t'hello\\nworld'"),
				(
						'def foo():\n\t\'docstring\'\n\t"hello\\nworld"',
						'def foo():\n\t\'docstring\'\n\t"hello\\nworld"'
						),
				('def foo():\n\t\'docstring\'\n\t"\\""', "def foo():\n\t'docstring'\n\t'\"'"),
				('def foo():\n\t\'docstring\'\n\t"quote \\""', "def foo():\n\t'docstring'\n\t'quote \"'"),
				("def foo():\n\t'docstring'\n\t'\\''", "def foo():\n\t'docstring'\n\t\"'\""),
				("def foo():\n\t'docstring'\n\t'quote \\''", "def foo():\n\t'docstring'\n\t\"quote '\""),
				(
						'def foo():\n\t\'docstring\'\n\tassert t.uname == "\\xe4\\xf6\\xfc"',
						'def foo():\n\t\'docstring\'\n\tassert t.uname == "äöü"'
						),
				(
						'def foo():\n\t\'docstring\'\n\tassert t.uname == "\\udce4\\udcf6\\udcfc"',
						'def foo():\n\t\'docstring\'\n\tassert t.uname == "\\udce4\\udcf6\\udcfc"'
						),
				]
		)
def test_quotes_function(value: str, expects: str):
	assert dynamic_quotes(value) == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				(
						"async def foo():\n\t'docstring'\n\t'hello world'",
						'async def foo():\n\t\'docstring\'\n\t"hello world"'
						),
				("async def foo():\n\t'docstring'\n\t''", "async def foo():\n\t'docstring'\n\t''"),
				('async def foo():\n\t\'docstring\'\n\t""', "async def foo():\n\t'docstring'\n\t''"),
				("async def foo():\n\t'docstring'\n\t'a'", "async def foo():\n\t'docstring'\n\t'a'"),
				('async def foo():\n\t\'docstring\'\n\t"a"', "async def foo():\n\t'docstring'\n\t'a'"),
				("async def foo():\n\t'docstring'\n\t'Z'", "async def foo():\n\t'docstring'\n\t'Z'"),
				('async def foo():\n\t\'docstring\'\n\t"Z"', "async def foo():\n\t'docstring'\n\t'Z'"),
				("async def foo():\n\t'docstring'\n\t'5'", "async def foo():\n\t'docstring'\n\t'5'"),
				('async def foo():\n\t\'docstring\'\n\t"5"', "async def foo():\n\t'docstring'\n\t'5'"),
				("async def foo():\n\t'docstring'\n\t'☃'", "async def foo():\n\t'docstring'\n\t'☃'"),
				("async def foo():\n\t'docstring'\n\t'user'", 'async def foo():\n\t\'docstring\'\n\t"user"'),
				('async def foo():\n\t\'docstring\'\n\t"☃"', "async def foo():\n\t'docstring'\n\t'☃'"),
				(
						'async def foo():\n\t\'docstring\'\n\tprint(123)\n"☃"',
						"async def foo():\n\t'docstring'\n\tprint(123)\n'☃'"
						),
				(
						'async def foo():\n\t\'docstring\'\n\t"☃"\nprint(123)',
						"async def foo():\n\t'docstring'\n\t'☃'\nprint(123)"
						),
				(
						"async def foo():\n\t'docstring'\n\t'hello\\nworld'",
						"async def foo():\n\t'docstring'\n\t'hello\\nworld'"
						),
				(
						'async def foo():\n\t\'docstring\'\n\t"hello\\nworld"',
						'async def foo():\n\t\'docstring\'\n\t"hello\\nworld"'
						),
				('async def foo():\n\t\'docstring\'\n\t"\\""', "async def foo():\n\t'docstring'\n\t'\"'"),
				(
						'async def foo():\n\t\'docstring\'\n\t"quote \\""',
						"async def foo():\n\t'docstring'\n\t'quote \"'"
						),
				("async def foo():\n\t'docstring'\n\t'\\''", "async def foo():\n\t'docstring'\n\t\"'\""),
				(
						"async def foo():\n\t'docstring'\n\t'quote \\''",
						"async def foo():\n\t'docstring'\n\t\"quote '\""
						),
				(
						'async def foo():\n\t\'docstring\'\n\tassert t.uname == "\\xe4\\xf6\\xfc"',
						'async def foo():\n\t\'docstring\'\n\tassert t.uname == "äöü"'
						),
				(
						'async def foo():\n\t\'docstring\'\n\tassert t.uname == "\\udce4\\udcf6\\udcfc"',
						'async def foo():\n\t\'docstring\'\n\tassert t.uname == "\\udce4\\udcf6\\udcfc"'
						),
				]
		)
def test_quotes_async_function(value: str, expects: str):
	assert dynamic_quotes(value) == expects
