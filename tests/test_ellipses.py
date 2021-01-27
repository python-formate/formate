# stdlib
from textwrap import dedent

# 3rd party
import pytest

# this package
from formate.ellipses import ellipsis_reformat

class_with_docstring = """
class F:
	'''
	Hello World
	'''
"""

class_with_body = """
class F:
	def foo():
		print('Hello World')
"""

class_with_method = """
class F:
	def foo():
		...
"""

class_with_method_expected = """
class F:
	def foo(): ...
"""

class_with_ellipsis = """
class F:
	...
"""

class_with_ellipsis_inline = """
class F: ...
"""

function_with_docstring = """
def foo():
	'''
	Hello World
	'''
"""

function_with_docstring_containing_stub = """
def foo():
	'''
	def bar():
		...
	'''
"""

function_with_body = """
def foo():
	print('Hello World')
"""

function_with_ellipsis = """
def foo():
	...
"""

function_with_ellipsis_inline = """
def foo(): ...
"""

async_function_with_docstring = """
async def foo():
	'''
	Hello World
	'''
"""

async_function_with_body = """
async def foo():
	print('Hello World')
"""

async_function_with_ellipsis = """
async def foo():
	...
"""

async_function_with_ellipsis_inline = """
async def foo(): ...
"""


@pytest.mark.parametrize(
		"code, expected",
		[
				pytest.param(class_with_docstring, class_with_docstring, id="class_with_docstring"),
				pytest.param(class_with_body, class_with_body, id="class_with_body"),
				pytest.param(class_with_method, class_with_method_expected, id="class_with_method"),
				pytest.param(class_with_ellipsis, class_with_ellipsis_inline, id="class_with_ellipsis"),
				pytest.param(
						class_with_ellipsis_inline,
						class_with_ellipsis_inline,
						id="class_with_ellipsis_inline",
						),
				pytest.param(function_with_docstring, function_with_docstring, id="function_with_docstring"),
				pytest.param(
						function_with_docstring_containing_stub,
						function_with_docstring_containing_stub,
						id="function_with_docstring_containing_stub"
						),
				pytest.param(function_with_body, function_with_body, id="function_with_body"),
				pytest.param(function_with_ellipsis, function_with_ellipsis_inline, id="function_with_ellipsis"),
				pytest.param(
						function_with_ellipsis_inline,
						function_with_ellipsis_inline,
						id="function_with_ellipsis_inline",
						),
				pytest.param(
						async_function_with_docstring,
						async_function_with_docstring,
						id="async_function_with_docstring",
						),
				pytest.param(async_function_with_body, async_function_with_body, id="async_function_with_body"),
				pytest.param(
						async_function_with_ellipsis,
						async_function_with_ellipsis_inline,
						id="async_function_with_ellipsis"
						),
				pytest.param(
						async_function_with_ellipsis_inline,
						async_function_with_ellipsis_inline,
						id="async_function_with_ellipsis_inline"
						),
				]
		)
def test_ellipsis_reformat(code: str, expected: str):
	assert ellipsis_reformat(code) == expected

	assert ellipsis_reformat(expected) == expected


def test_ellipsis_reformat_return_ann():
	code = ["def foo() -> str:", "\t..."]
	expected = ["def foo() -> str: ..."]
	assert ellipsis_reformat('\n'.join(code)) == '\n'.join(expected)


def test_ellipsis_reformat_multiple():
	code = dedent("""\
def foo():
	...


def bar():
	...


class F:
	...


class FizzBuzz:
	...
""")

	expected = dedent("""\
def foo(): ...


def bar(): ...


class F: ...


class FizzBuzz: ...
""")

	assert ellipsis_reformat(code) == expected


def test_ellipsis_reformat_no_op():
	code = ["def foo() -> str:", "\tpass"]
	assert ellipsis_reformat('\n'.join(code)) == '\n'.join(code)

