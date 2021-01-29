#!/usr/bin/env python3
#
#  mini_hooks.py
"""
Small but mighty hooks.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import ast
import re

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike

# this package
from formate.config import wants_filename

__all__ = ["noqa_reformat", "check_ast", "squish_stubs"]


def noqa_reformat(source: str) -> str:
	"""
	Pull ``# noqa: ...`` comments that immediately follow docstrings back up to the end of the correct line.

	:param source: The source to reformat.

	:return: The reformatted source.
	"""

	return re.sub(r'"""[\n\s]+#\s+noqa', '"""  # noqa', source)


def check_ast(source: str) -> str:
	"""
	Check the source can be parsed as a Python Abstract Syntax Tree.

	:param source: The source to check.

	:raises SyntaxError: If the source is not valid Python.

	:return: The source unchanged.
	"""

	ast.parse(source)
	return source


@wants_filename
def squish_stubs(source: str, formate_filename: PathLike) -> str:
	"""
	Squash type stubs by removing unnecessary blank lines.

	.. versionadded:: 0.2.0

	:param source: The source to check.
	:param formate_filename: The name of the source file, to ensure this hook only runs on type stubs.

	:return: The reformatted source.
	"""

	def_re = re.compile(r"^(?:# )?(\s*)def( .*\($)?")
	deco_re = re.compile(r"^(?:# )?(\s*)@")

	filename = PathPlus(formate_filename)

	if filename.suffix != ".pyi":
		return source

	source_lines = source.split('\n')
	reformatted_lines = StringList()

	last_line = ''
	in_indented_block = ''

	for line in source_lines:
		line_m = def_re.match(line)
		last_line_m = def_re.match(last_line)
		deco_m = deco_re.match(line)

		if line_m and line_m.group(2):
			in_indented_block = line_m.group(1)

		if last_line_m:

			if line_m and last_line_m.group(1) == line_m.group(1):
				last_line = line
				reformatted_lines.append(line)
			elif not line:
				in_indented_block = ''
				continue
			elif deco_m and last_line_m.group(1) == deco_m.group(1):
				last_line = line

				reformatted_lines.blankline(ensure_single=True)
				reformatted_lines.append(line)
			else:
				last_line = line

				if not in_indented_block:
					reformatted_lines.blankline(ensure_single=True)
					reformatted_lines.blankline()

				reformatted_lines.append(line)

		elif deco_m and deco_m.group(1):
			last_line = line

			reformatted_lines.blankline(ensure_single=True)
			reformatted_lines.append(line)
		else:
			last_line = line
			reformatted_lines.append(line)

	reformatted_lines.blankline(ensure_single=True)

	return str(reformatted_lines)
