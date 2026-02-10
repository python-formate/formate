# stdlib
import re
import shutil
from typing import List, Mapping, Union, no_type_check

# 3rd party
import pytest
from _pytest.capture import CaptureResult
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from coincidence.selectors import max_version, min_version, not_pypy, only_pypy
from consolekit.terminal_colours import strip_ansi
from consolekit.testing import CliRunner, Result, click_version
from domdf_python_tools.paths import PathPlus, in_directory
from domdf_python_tools.typing import PathLike

# this package
import formate
from formate import Reformatter, reformat_file
from formate.__main__ import main
from formate.classes import EntryPoint, Hook
from formate.config import formats_filetypes, load_toml, wants_filename

path_sub = re.compile(r" .*/pytest-of-.*/pytest-\d+")


@no_type_check
def check_out(
		result: Union[Result, CaptureResult[str]],
		advanced_data_regression: AdvancedDataRegressionFixture,
		) -> None:

	if hasattr(result, "stdout"):
		stdout = result.stdout
	else:
		stdout = result.out

	if hasattr(result, "stderr"):
		stderr = result.stderr
	else:
		stderr = result.err

	data_dict = {
			"out": strip_ansi(path_sub.sub(" ...", stdout)).split('\n'),
			"err": strip_ansi(path_sub.sub(" ...", stderr)).split('\n'),
			}

	advanced_data_regression.check(data_dict)


@pytest.fixture()
def demo_environment(tmp_pathplus: PathPlus) -> None:

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
			r"assert t.uname == '\udce4\udcf6\udcfc'",
			]

	(tmp_pathplus / "code.py").write_lines(code, trailing_whitespace=True)


@pytest.fixture()
def demo_pyproject_environment(demo_environment: None, tmp_pathplus: PathPlus) -> None:
	example_formate_toml = PathPlus(__file__).parent / "example_pyproject.toml"
	(tmp_pathplus / "pyproject.toml").write_text(example_formate_toml.read_text())


@pytest.mark.usefixtures("demo_environment")
def test_integration(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	config = load_toml(tmp_pathplus / "formate.toml")

	st = (tmp_pathplus / "code.py").stat()
	assert st == st

	assert reformat_file(tmp_pathplus / "code.py", config) == 1
	advanced_file_regression.check_file(tmp_pathplus / "code.py")
	check_out(capsys.readouterr(), advanced_data_regression)

	# mtime should have changed
	new_st = (tmp_pathplus / "code.py").stat()
	assert new_st.st_mtime != st.st_mtime
	assert new_st != st

	# Calling a second time shouldn't change anything
	assert reformat_file(tmp_pathplus / "code.py", config) == 0
	advanced_file_regression.check_file(tmp_pathplus / "code.py")

	# mtime should be the same
	assert (tmp_pathplus / "code.py").stat().st_mtime == new_st.st_mtime


@pytest.mark.usefixtures("demo_pyproject_environment")
def test_integration_pyproject(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	config = load_toml(tmp_pathplus / "pyproject.toml")

	assert reformat_file(tmp_pathplus / "code.py", config) == 1
	advanced_file_regression.check_file(tmp_pathplus / "code.py")
	check_out(capsys.readouterr(), advanced_data_regression)

	# Calling a second time shouldn't change anything
	assert reformat_file(tmp_pathplus / "code.py", config) == 0
	advanced_file_regression.check_file(tmp_pathplus / "code.py")


@pytest.mark.usefixtures("demo_environment")
def test_reformatter_class(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	config = load_toml(tmp_pathplus / "formate.toml")

	r = Reformatter(tmp_pathplus / "code.py", config)

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.to_string()

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.to_file()

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.get_diff()

	st = (tmp_pathplus / "code.py").stat()
	assert st == st

	assert r.run() == 1
	r.to_file()

	advanced_file_regression.check_file(tmp_pathplus / "code.py")
	advanced_file_regression.check(r.to_string(), extension="._py_")

	captured = capsys.readouterr()

	assert not captured.out
	assert not captured.err

	# mtime should have changed
	new_st = (tmp_pathplus / "code.py").stat()
	assert new_st.st_mtime != st.st_mtime
	assert new_st != st

	# Calling a second time shouldn't change anything
	r = Reformatter(tmp_pathplus / "code.py", config)
	assert r.run() == 0
	r.to_file()

	advanced_file_regression.check_file(tmp_pathplus / "code.py")


@pytest.mark.usefixtures("demo_environment")
def test_reformatter_class_non_python_hook(
		tmp_pathplus: PathPlus,
		monkeypatch,
		):

	config = load_toml(tmp_pathplus / "formate.toml")
	config["hooks"]["format-foo"] = {"priority": 10}  # type: ignore[index]

	(tmp_pathplus / "code.foo").touch()

	@formats_filetypes(".foo")
	@wants_filename
	def format_foo(source: str, formate_filename: PathLike) -> str:
		return "Result of format-foo"

	def parse_hooks(config: Mapping) -> List[Hook]:
		return [Hook(name="format-foo", entry_point=EntryPoint("format-foo", format_foo))]

	monkeypatch.setattr(formate, "parse_hooks", parse_hooks)
	r = Reformatter(tmp_pathplus / "code.foo", config)

	assert r.run()
	assert r.to_string() == "Result of format-foo\n"


@pytest.mark.usefixtures("demo_environment")
def test_cli(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result

	st = (tmp_pathplus / "code.py").stat()
	assert st == st

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "--no-colour", "--diff", "--verbose"],
				)

	assert result.exit_code == 1

	advanced_file_regression.check_file(tmp_pathplus / "code.py")

	check_out(result, advanced_data_regression)

	# mtime should have changed
	new_st = (tmp_pathplus / "code.py").stat()
	assert new_st.st_mtime != st.st_mtime
	assert new_st != st

	# Calling a second time shouldn't change anything
	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["code.py"])

	assert result.exit_code == 0

	# mtime should be the same
	assert (tmp_pathplus / "code.py").stat().st_mtime == new_st.st_mtime


@pytest.mark.usefixtures("demo_environment")
def test_cli_verbose_verbose(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 1

	advanced_file_regression.check_file(tmp_pathplus / "code.py")

	# Calling a second time shouldn't change anything
	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "code.c", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 0

	check_out(result, advanced_data_regression)


@pytest.mark.usefixtures("demo_environment")
def test_cli_verbose_verbose_no_supported_hooks(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result
	(tmp_pathplus / "code.c").touch()
	(tmp_pathplus / "a_dir").mkdir()

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "a_dir", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 1

	advanced_file_regression.check_file(tmp_pathplus / "code.py")

	# Calling a second time shouldn't change anything
	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "code.c", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 0

	check_out(result, advanced_data_regression)


@pytest.mark.usefixtures("demo_environment")
def test_cli_verbose_verbose_unicode_error(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result
	shutil.copy2(PathPlus(__file__).parent / "image.png", tmp_pathplus / "image.png")

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "image.png", "--no-colour", "--diff", "--verbose", "-v"],
				)

	assert result.exit_code == 1

	check_out(result, advanced_data_regression)


@pytest.mark.usefixtures("demo_environment")
@max_version("3.9.9", reason="Output differs on Python 3.10+")
@not_pypy("Output differs on PyPy")
def test_cli_syntax_error(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
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

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result: Result = runner.invoke(main, args=["code.py", "--no-colour", "--verbose"])

	assert result.exit_code == 126

	check_out(result, advanced_data_regression)


@pytest.mark.usefixtures("demo_environment")
@only_pypy("Output differs on PyPy")
def test_cli_syntax_error_pypy(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
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

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result: Result = runner.invoke(main, args=["code.py", "--no-colour", "--verbose"])

	assert result.exit_code == 126

	check_out(result, advanced_data_regression)


@pytest.mark.usefixtures("demo_environment")
@min_version("3.10", reason="Output differs on Python 3.10+")
def test_cli_syntax_error_py310(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
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

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result: Result = runner.invoke(main, args=["code.py", "--no-colour", "--verbose"])

	assert result.exit_code == 126

	check_out(result, advanced_data_regression)


@pytest.mark.skipif(click_version[0] != 7, reason="Output differs on Click 8")
def test_cli_no_config(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["--no-colour", "--verbose"])

	assert result.exit_code == 2

	check_out(result, advanced_data_regression)


@pytest.mark.skipif(click_version[0] == 7, reason="Output differs on Click 8")
def test_cli_no_config_click8(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(main, args=["--no-colour", "--verbose"])

	assert result.exit_code == 2

	check_out(result, advanced_data_regression)
