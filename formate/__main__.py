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
import sys

# 3rd party
import click
from consolekit import click_command
from consolekit.options import colour_option, verbose_option

if False:
	# stdlib
	from typing import List, Optional

	# 3rd party
	from consolekit.terminal_colours import ColourTrilean

__all__ = ["main"]


@colour_option()
@verbose_option()
@click.option(
		"-e",
		"--exclude",
		metavar="PATTERN",
		type=list,
		default=None,
		help="Patterns for files to exclude from formatting.",
		)
@click.option(
		"-c",
		"--config-file",
		type=click.STRING,
		help="The path to the TOML configuration file to use.",
		default="formate.toml",
		show_default=True,
		)
@click.argument("filename", type=click.STRING, nargs=-1)
@click_command()
def main(
		filename: str,
		config_file: str,
		exclude: "Optional[List[str]]",
		colour: "ColourTrilean" = None,
		verbose: bool = False,
		):
	"""
	Reformat the given Python source files.
	"""

	# stdlib
	import fnmatch
	import re

	# this package
	from formate import reformat_file
	from formate.config import load_toml

	retv = 0

	try:
		config = load_toml(config_file)
	except FileNotFoundError:
		raise click.UsageError("'formate.toml' not found.")

	for path in filename:
		for pattern in exclude or []:
			if re.match(fnmatch.translate(pattern), str(path)):
				continue

		ret_for_file = reformat_file(path, config=config, colour=colour)
		if ret_for_file == 1 and verbose:
			click.echo(f"Reformatting {path}.")
		elif verbose > 1:
			click.echo(f"Checking {path}.")

		retv |= ret_for_file

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())
