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
				]
		)
def test_quotes(value: str, expects: str):
	assert dynamic_quotes(value) == expects
