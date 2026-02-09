# stdlib
from textwrap import dedent

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture

# this package
from formate.mini_hooks import check_ast, newline_after_equals, noqa_reformat, squish_stubs


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


def test_squish_stubs(advanced_file_regression: AdvancedFileRegressionFixture):
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


		def unregister(self, cls: Type) -> Any: ...

		registry: Mapping[Any, Callable[..., _T]]


	@sphinxify_json_docstring()
	@append_docstring_from(json.loads)
	def load(
			fp: SupportsRead[_LoadsString],
			*,
			cls: Optional[Type[json.JSONDecoder]] = ...,
			object_hook: Optional[Callable[[Dict[Any, Any]], Any]] = ...,
			parse_float: Optional[Callable[[str], Any]] = ...,
			parse_int: Optional[Callable[[str], Any]] = ...,
			parse_constant: Optional[Callable[[str], Any]] = ...,
			object_pairs_hook: Optional[Callable[[List[Tuple[Any, Any]]], Any]] = ...,
			**kwargs: Any
			) -> Any: ...



	class MissingObjectFinder:
		object_store: Any = ...
		sha_done: Any = ...

		def __init__(self): ...

		def add_todo(self, entries: Any) -> None: ...

		def next(self): ...
		__next__: Any = ...

	class MissingObjectFinder:

		def __init__(self): ...

		def add_todo(self, entries: Any) -> None: ...

		def next(self): ...
		__next__: Any = ...

	class DivergedBranches(Error): ...
	def check_diverged(repo: Repo, current_sha: Any, new_sha: Any) -> None: ...

	''',
			)

	advanced_file_regression.check(squish_stubs(source, "file.pyi"), extension="._py_")


def test_squish_stubs_not_pyi():
	code = """
	def foo():
		...
	"""

	new_code = squish_stubs(code, formate_filename="code.pyi")
	assert new_code != code

	with pytest.raises(ValueError, match=r"Unsupported filetype '\.py'"):
		squish_stubs(code, formate_filename="code.py")


newline_after_equals_src = """
def foo():

	with pytest.raises(
			ValueError,
			match=
			"This is a really long error message that exceeds the line length limit so gets pushed down!!!!!!",
			):
		pass

"""

no_newline_after_equals_src = """
def foo():

	with pytest.raises(
			ValueError,
			match="This is a shorter error message that's still too long to fit on one line.",
			):
		pass

"""


def test_newline_after_equals(advanced_file_regression: AdvancedFileRegressionFixture):

	advanced_file_regression.check(newline_after_equals(newline_after_equals_src))
	assert newline_after_equals(no_newline_after_equals_src) == no_newline_after_equals_src

	src = """
def foo():
	directive = SimpleNamespace()
"""

	assert newline_after_equals(src) == src
