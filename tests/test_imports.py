# 3rd party
import pytest
from coincidence import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from formate.imports import CollectionsABCRewriter, rewrite_collections_abc_imports

params = pytest.mark.parametrize(
		"code",
		[
				pytest.param("from collections import (\nIterable,\nCounter,\n)", id="top_level"),
				pytest.param(
						"# code.py\n__all__ = ['foo', 'bar']\n\nfrom collections import (\nIterable,\nCounter,\n)",
						id="top_level_code_before"
						),
				pytest.param(
						"from collections import (\nIterable,\nCounter,\n)\nfrom .. import bar\nfrom . import baz\n",
						id="top_level_relative"
						),
				pytest.param("class F:\n\tfrom collections import (\nIterable,\nCounter,\n)", id="in_class_tabs"),
				pytest.param(
						"def foo():\n\tfrom collections import (\nIterable,\nCounter,\n)", id="in_function_tabs"
						),
				pytest.param(
						"class F:\n    from collections import (\nIterable,\nCounter,\n)", id="in_class_spaces"
						),
				pytest.param(
						"def foo():\n    from collections import (\nIterable,\nCounter,\n)",
						id="in_function_spaces"
						),
				pytest.param(
						"def foo():\n    from collections import (\nIterable,\nCounter,\n)\n    from typing import List",
						id="in_function_another_import"
						),
				]
		)


@params
def test_rewrite_collections_abc_imports(code, file_regression: FileRegressionFixture):
	check_file_regression(rewrite_collections_abc_imports(code), file_regression, extension="._py")


@params
def test_CollectionsABCRewriter(code, file_regression: FileRegressionFixture):
	check_file_regression(CollectionsABCRewriter(code).rewrite(), file_regression, extension="._py")
