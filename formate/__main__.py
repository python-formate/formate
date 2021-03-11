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
from typing import Iterable, List, Optional

# 3rd party
import click
from consolekit import click_command
from consolekit.options import MultiValueOption, colour_option, flag_option, verbose_option
from consolekit.terminal_colours import ColourTrilean, resolve_color_default
from consolekit.tracebacks import handle_tracebacks, traceback_option
from domdf_python_tools.typing import PathLike

# this package
from formate import Reformatter

__all__ = ["main"]


@flag_option("--diff", "show_diff", help="Show a diff of changes made")
@traceback_option()
@colour_option()
@verbose_option()
@click.option(
		"-e",
		"--exclude",
		metavar="PATTERN",
		type=click.STRING,
		cls=MultiValueOption,
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
		filename: Iterable[PathLike],
		config_file: PathLike,
		exclude: "Optional[List[str]]",
		colour: "ColourTrilean" = None,
		verbose: bool = False,
		show_traceback: bool = False,
		show_diff: bool = False,
		):
	"""
	Reformat the given Python source files.
	"""

	# stdlib
	import fnmatch
	import re

	# 3rd party
	from domdf_python_tools.paths import PathPlus

	# this package
	from formate.config import load_toml
	from formate.utils import SyntaxTracebackHandler, syntaxerror_for_file

	retv = 0

	try:
		config = load_toml(config_file)
	except FileNotFoundError:
		raise click.UsageError(f"Config file '{config_file}' not found")

	for path in filename:
		for pattern in exclude or []:
			if re.match(fnmatch.translate(pattern), str(path)):
				continue

		path = PathPlus(path)

		if path.suffix not in {".py", ".pyi", ''} or path.is_dir():
			if verbose >= 2:
				click.echo(f"Skipping {path} as it doesn't appear to be a Python file")

			continue

		r = Reformatter(path, config=config)

		with handle_tracebacks(show_traceback, cls=SyntaxTracebackHandler):
			with syntaxerror_for_file(path):
				ret_for_file = r.run()

		if ret_for_file:
			if verbose:
				click.echo(f"Reformatting {path}")
			if show_diff:
				click.echo(r.get_diff(), color=resolve_color_default(colour))

			r.to_file()

		elif verbose >= 2:
			click.echo(f"Checking {path}")

		retv |= ret_for_file

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())
