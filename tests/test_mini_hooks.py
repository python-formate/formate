# stdlib
from textwrap import dedent

# 3rd party
import pytest
from coincidence import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from formate.mini_hooks import check_ast, noqa_reformat, squish_stubs


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


def test_squish_stubs(file_regression: FileRegressionFixture):
	source = dedent(
			'''\
	#!/usr/bin/env python3
	#
	#  __init__.py
	"""
	Type stubs for appdirs
	"""
	#

	ColourTrilean = Optional[bool]

	CSI: Final[str]
	OSC: Final[str]
	BEL: Final[str]

	fore_stack: Deque[str]
	back_stack: Deque[str]
	style_stack: Deque[str]


	def resolve_color_default(color: Optional[bool] = ...) -> Optional[bool]: ...


	def code_to_chars(code) -> str: ...


	def set_title(title: str) -> str: ...


	# def clear_screen(mode: int = ...) -> str: ...
	def clear_line(mode: int = ...) -> str: ...


	def strip_ansi(value: str) -> str: ...


	_C = TypeVar("_C", bound="Colour")


	class Colour(str):
		style: str
		reset: str
		stack: Union[Deque[str], List[str]]

		def __new__(cls, style: str, stack: Union[Deque[str], List[str]], reset: str) -> "Colour": ...

		def __enter__(self) -> None: ...

		def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

		def __call__(self, text) -> str: ...


		@classmethod
		def from_code(cls: Type[_C], code: Union[str, int], background: bool = ...) -> _C: ...




		@classmethod
		def from_rgb(
				cls: Type[_C],
				r: Union[str, int],
				g: Union[str, int],
				b: Union[str, int],
				background: bool = ...
				) -> _C: ...


		@classmethod
		def from_hex(cls: Type[_C], hex_colour: str, background: bool = ...) -> _C: ...


	def print_256_colour_testpattern() -> None: ...



	def print_512_colour_testpattern() -> None: ...


	class AnsiCodes(ABC):
		_stack: Union[Deque[str], List[str]]
		_reset: str

		def __init__(self) -> None: ...



	@overload
	def foo(hex_colour: str, background: Literal[True] = ...) -> _C: ...

	@overload
	def foo(hex_colour: str, background: Literal[True] = ...) -> _D: ...


	def user_data_dir(
			appname: Optional[str] = ...,
			appauthor: Optional[str] = ...,
			version: Optional[str] = ...,
			roaming: bool = ...,
			) -> str: ...

	def print_512_colour_testpattern() -> None: ...


	def user_data_dir(
			appname: Optional[str] = ...,
			appauthor: Optional[str] = ...,
			version: Optional[str] = ...,
			roaming: bool = ...,
			) -> str: ...

	class Foo:

		def check(
			self,
			data_dict: Union[Sequence, Mapping],
			basename: Optional[str] = ...,
			fullpath: Optional[str] = ...,
			) -> None: ...

		# non-PEP 8 alias used internally at ESSS
		Check = check


	'''
			)

	check_file_regression(squish_stubs(source, "file.pyi"), file_regression, extension="._py_")
