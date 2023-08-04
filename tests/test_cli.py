# stdlib
import re
import sys
from typing import Optional

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit.testing import CliRunner
from domdf_python_tools.words import LF

# this package
import formate
from formate.__main__ import main


def test_help(advanced_file_regression: AdvancedFileRegressionFixture):

	runner = CliRunner()

	result = runner.invoke(main, catch_exceptions=False, args="--help")
	assert result.exit_code == 0
	result.check_stdout(advanced_file_regression)


def test_version():

	runner = CliRunner()

	result = runner.invoke(main, catch_exceptions=False, args="--version")
	assert result.exit_code == 0
	assert result.stdout == f"formate version {formate.__version__}\n"

	result = runner.invoke(main, catch_exceptions=False, args=["--version", "--version"])
	assert result.exit_code == 0
	assert result.stdout == f"formate version {formate.__version__}, Python {sys.version.replace(LF, ' ')}\n"
