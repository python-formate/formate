#!/usr/bin/env python3
#
#  __main__.py
"""
CLI entry point.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import fnmatch
import re
import sys
from typing import List, Optional

# 3rd party
import click
import toml
from consolekit import click_command
from domdf_python_tools.paths import PathPlus

# this package
from formate import FormateConfigDict, call_hooks, reformat_file
from formate.config import load_toml, parse_hooks

__all__ = ["main"]


@click.argument("filename", type=click.STRING, nargs=-1)
@click.option(
		"-c",
		"--config-file",
		type=click.STRING,
		help="The path to the TOML configuration file to use.",
		default="formate.toml",
		show_default=True,
		)
@click.option(
		"-e",
		"--exclude",
		metavar="PATTERN",
		type=list,
		default=None,
		help="patterns for files to exclude from formatting",
		)
@click_command()
def main(
		filename: str,
		config_file: str,
		exclude: Optional[List[str]],
		):
	"""
	Reformat the given Python source files.
	"""

	retv = 0

	config = load_toml(config_file)

	for path in filename:
		for pattern in exclude or []:
			if re.match(fnmatch.translate(pattern), str(path)):
				continue

		retv |= reformat_file(path, config=config)

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())

# hooks = parse_hooks(config)
#
# for hook in hooks:
# 	print(hook)
#
# print()
#
# source = """\
# class F:
# 	from collections import (
# Iterable,
# 	Counter,
# 		)
#
# print('hello world')
# """
#
# reformatted_source = call_hooks(hooks, source)
# print(reformatted_source)
