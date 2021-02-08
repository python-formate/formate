# 3rd party
from domdf_python_tools.stringlist import StringList
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from formate import isort_hook


def test_isort_stubs(file_regression: FileRegressionFixture):
	source = StringList([
			'from natsort.natsort import as_ascii as as_ascii, as_utf8 as as_utf8, decoder as decoder, humansorted as '
			'humansorted, index_humansorted as index_humansorted, index_natsorted as index_natsorted, index_realsorted as '
			'index_realsorted, natsort_key as natsort_key, natsort_keygen as natsort_keygen, natsorted as natsorted, ns as ns, '
			'numeric_regex_chooser as numeric_regex_chooser, order_by_index as order_by_index, os_sort_key as os_sort_key, '
			'os_sort_keygen as os_sort_keygen, os_sorted as os_sorted, realsorted as realsorted',
			"from natsort.utils import chain_functions as chain_functions",
			'',
			])
	file_regression.check(isort_hook(str(source), "utils.pyi"))
