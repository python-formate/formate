# 3rd party
import pytest
from coincidence import check_file_regression
from domdf_python_tools.stringlist import StringList
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from formate.reformat_generics import reformat_generics

example_1 = """
_ConvertibleType = Union[
		type,
		ParamType,
		Tuple[Union[type, ParamType], ...],
		Callable[[str], Any],
		Callable[[Optional[str]], Any],
		]
"""

example_1a = """
_ConvertibleType = Union[type, ParamType, Tuple[Union[type, ParamType], ...], Callable[[str], Any], Callable[[Optional[str]], Any]]
"""

example_2 = """
_ParamsType = Optional[Union[Mapping[Union[str, bytes, int, float], "_ParamsMappingValueType"],
								Union[str, bytes],
								Tuple[Union[str, bytes, int, float], "_ParamsMappingValueType"], ]]
"""

example_3 = """
dtype = Literal["sphinx_rtd_theme", "sphinx-rtd-theme", "alabaster", "repo_helper_sphinx_theme",
				"repo-helper-sphinx-theme", "domdf_sphinx_theme", "domdf-sphinx-theme", "furo"]
"""

example_4 = """
class Foo:
	dtype = Literal["sphinx_rtd_theme", "sphinx-rtd-theme", "alabaster", "repo_helper_sphinx_theme",
					"repo-helper-sphinx-theme", "domdf_sphinx_theme", "domdf-sphinx-theme", "furo"]
"""

example_5 = """
class Foo:
	dtype = typing.Union[typing.List, typing.Tuple, typing.Mapping, typing.MutableMapping, typing.Counter, typing.ChainMap, typing.Collection, foo.bar.baz]
"""


@pytest.mark.parametrize(
		"code",
		[
				pytest.param("Union[str, int, float]", id="Simple Union"),
				pytest.param("Mapping[str, int]", id="Simple Mapping"),
				pytest.param("List[str]", id="Simple List"),
				pytest.param("Tuple[int, int, str, float, str, int, bytes]", id="Simple Tuple"),
				pytest.param(
						"Tuple[int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes]",
						id="Long Tuple"
						),
				pytest.param("Optional[Callable[[Optional[str]], Any]]", id="Complex Optional"),
				pytest.param(
						"_ParamsMappingValueType = Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]]",
						id="Complex Alias 1"
						),
				pytest.param(
						"_Data = Union[None, str, bytes, MutableMapping[str, Any], Iterable[Tuple[str, Optional[str]]], IO]",
						id="Complex Alias 2"
						),
				pytest.param(example_1, id="Multiline 1"),
				pytest.param(example_1a, id="Multiline 1a"),
				pytest.param(example_2, id="Multiline 2"),
				pytest.param(example_3, id="Literal"),
				pytest.param(example_4, id="Literal in class"),
				pytest.param(example_5, id="Union in class"),
				]
		)
def test_generics(code, file_regression: FileRegressionFixture):
	check_file_regression(reformat_generics(code), file_regression, extension="._py")


def test_generics_functions(file_regression: FileRegressionFixture):
	code = StringList([
			"def foo():",
			"\tdata: Tuple[int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes] = ()",
			'',
			"async def acync_foo():",
			"\tdata: Tuple[int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes] = ()",
			])

	check_file_regression(reformat_generics(str(code)), file_regression, extension="._py")
