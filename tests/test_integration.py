# stdlib
import re

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture, check_file_output, check_file_regression
from coincidence.selectors import not_pypy, only_pypy
from consolekit.terminal_colours import strip_ansi
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus, in_directory
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from formate import Reformatter, reformat_file
from formate.__main__ import main
from formate.config import load_toml

path_sub = re.compile(rf" .*/pytest-of-.*/pytest-\d+")


@pytest.fixture()
def demo_environment(tmp_pathplus):

	example_formate_toml = PathPlus(__file__).parent / "example_formate.toml"
	(tmp_pathplus / "formate.toml").write_text(example_formate_toml.read_text())

	code = [
			"class F:",
			"\tfrom collections import (",
			"Iterable,",
			"\tCounter,",
			"\t\t)",
			'',
			"\tdef foo(self):",
			"\t\tpass",
			'',
			"print('hello world')",
			]

	(tmp_pathplus / "code.py").write_lines(code, trailing_whitespace=True)


def test_integration(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		demo_environment,
		):

	config = load_toml(tmp_pathplus / "formate.toml")

	assert reformat_file(tmp_pathplus / "code.py", config) == 1

	check_file_output(tmp_pathplus / "code.py", file_regression)
	captured = capsys.readouterr()

	data_dict = {
			"out": strip_ansi(path_sub.sub(" ...", captured.out)).split('\n'),
			"err": strip_ansi(path_sub.sub(" ...", captured.err)).split('\n')
			}

	advanced_data_regression.check(data_dict)

	# Calling a second time shouldn't change anything
	assert reformat_file(tmp_pathplus / "code.py", config) == 0

	check_file_output(tmp_pathplus / "code.py", file_regression)


def test_reformatter_class(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		demo_environment,
		):

	config = load_toml(tmp_pathplus / "formate.toml")

	r = Reformatter(tmp_pathplus / "code.py", config)

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.to_string()

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.to_file()

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.get_diff()

	assert r.run() == 1
	r.to_file()

	check_file_output(tmp_pathplus / "code.py", file_regression)
	check_file_regression(r.to_string(), file_regression, extension="._py_")

	captured = capsys.readouterr()

	assert not captured.out
	assert not captured.err

	# Calling a second time shouldn't change anything
	assert reformat_file(tmp_pathplus / "code.py", config) == 0

	check_file_output(tmp_pathplus / "code.py", file_regression)


def test_cli(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		demo_environment,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "--no-colour", "--diff", "--verbose"],
				)

	assert result.exit_code == 1

	check_file_output(tmp_pathplus / "code.py", file_regression)

	data_dict = {
			"out": path_sub.sub(" ...", result.stdout).split('\n'),
			"err": path_sub.sub(" ...", result.stderr).split('\n'),
			}

	advanced_data_regression.check(data_dict)

	# Calling a second time shouldn't change anything
	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["code.py"])

	assert result.exit_code == 0


def test_cli_verbose_verbose(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		demo_environment,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 1

	check_file_output(tmp_pathplus / "code.py", file_regression)

	# Calling a second time shouldn't change anything
	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "code.c", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 0

	data_dict = {
			"out": path_sub.sub(" ...", result.stdout).split('\n'),
			"err": path_sub.sub(" ...", result.stderr).split('\n'),
			}

	advanced_data_regression.check(data_dict)


@not_pypy("Output differs on PyPy")
def test_cli_syntax_error(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		demo_environment,
		):

	code = [
			"class F:",
			"\tfrom collections import (",
			"Iterable,",
			"\tCounter,",
			"\t\t)",
			'',
			"\tdef foo(self):",
			"\t\tpass",
			'',
			"print('hello world'",
			]

	(tmp_pathplus / "code.py").write_lines(code, trailing_whitespace=True)

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["code.py", "--no-colour", "--verbose"])

	assert result.exit_code == 126

	data_dict = {
			"out": path_sub.sub(" ...", result.stdout).split('\n'),
			"err": path_sub.sub(" ...", result.stderr).split('\n'),
			}

	advanced_data_regression.check(data_dict)


@only_pypy("Output differs on PyPy")
def test_cli_syntax_error_pypy(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		demo_environment,
		):

	code = [
			"class F:",
			"\tfrom collections import (",
			"Iterable,",
			"\tCounter,",
			"\t\t)",
			'',
			"\tdef foo(self):",
			"\t\tpass",
			'',
			"print('hello world'",
			]

	(tmp_pathplus / "code.py").write_lines(code, trailing_whitespace=True)

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["code.py", "--no-colour", "--verbose"])

	assert result.exit_code == 126

	data_dict = {
			"out": path_sub.sub(" ...", result.stdout).split('\n'),
			"err": path_sub.sub(" ...", result.stderr).split('\n'),
			}

	advanced_data_regression.check(data_dict)


def test_cli_no_config(
		tmp_pathplus: PathPlus,
		file_regression: FileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["--no-colour", "--verbose"])

	assert result.exit_code == 2

	data_dict = {
			"out": path_sub.sub(" ...", result.stdout).split('\n'),
			"err": path_sub.sub(" ...", result.stderr).split('\n'),
			}

	advanced_data_regression.check(data_dict)
