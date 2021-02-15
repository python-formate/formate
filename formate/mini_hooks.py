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
from typing import List

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

	filename = PathPlus(formate_filename)

	if filename.suffix != ".pyi":
		return source

	blocks = _breakup_source(source)
	return str(_reformat_blocks(blocks))


class _Variables(list):
	pass


class _Class(list):
	pass


class _Function(list):
	pass


class _DecoratedFunction(_Function):
	pass


class _Decorator(list):
	pass


class _MultilineFunction(_Function):
	pass


def _breakup_source(source: str) -> List[List[str]]:
	blocks: List[List[str]] = [[]]

	for line in source.split('\n'):
		if not line.strip():
			if isinstance(blocks[-1], _Variables):
				blocks[-1].append(line)

		elif line.lstrip().startswith('@'):
			if isinstance(blocks[-1], _Decorator):
				blocks[-1].append(line)
			else:
				blocks.append(_Decorator([line]))

		elif line.lstrip().startswith("def "):
			if isinstance(blocks[-1], _Decorator):
				blocks[-1] = _DecoratedFunction([*blocks[-1], line])
			else:
				blocks.append(_Function([line]))

		elif line.lstrip().startswith("class "):
			# TODO: decorated classes?
			blocks.append(_Class([line]))

		elif line.rstrip().startswith(' ') or line.startswith('\t'):
			if isinstance(blocks[-1], _Class):
				blocks[-1].append(line)
			elif isinstance(blocks[-1], _MultilineFunction):
				if len(blocks[-1]) < 2:
					blocks[-1].append(line)
				elif re.split("[A-Za-z)*_]", line)[0] == re.split("[A-Za-z)*_]", blocks[-1][-1])[0]:
					blocks[-1].append(line)
				else:
					blocks.append(_Variables([line]))
			elif isinstance(blocks[-1], _Function):
				if re.split("[A-Za-z]", line)[0] == re.split("[A-Za-z]", blocks[-1][-1])[0]:
					blocks.append(_Variables([line]))
				elif line.rstrip().endswith(','):
					blocks[-1] = _MultilineFunction([*blocks[-1], line])
				else:
					blocks.append(_Variables([line]))

			elif isinstance(blocks[-1], _Variables):
				blocks[-1].append(line)
			else:
				blocks.append(_Variables([line]))

		else:
			if isinstance(blocks[-1], _Variables):
				blocks[-1].append(line)
			else:
				blocks.append(_Variables([line]))

	return blocks


def _reformat_blocks(blocks: List[List[str]]):

	cursor = 1

	while cursor < len(blocks):

		if isinstance(blocks[cursor - 1], (_MultilineFunction, _DecoratedFunction, _Class)):
			# Add a blank line after _Variables, a multi-line function, or a decorated function
			blocks.insert(cursor, [])
			cursor += 1

		if blocks[cursor] and blocks[cursor - 1] and re.match("^[ \t]+", blocks[cursor - 1][-1]
																) and not re.match("^[ \t]+", blocks[cursor][0]):
			# Add a blank line after a dedent
			blocks.insert(cursor, [])
			cursor += 1

		if isinstance(blocks[cursor - 1], _Variables):
			# Add a blank line before and after _Variables
			blocks.insert(cursor - 1, [])
			blocks.insert(cursor + 1, [])
			cursor += 2

		if isinstance(blocks[cursor], _Variables):
			# Add a blank line before and after _Variables
			blocks.insert(cursor, [])
			blocks.insert(cursor + 2, [])
			cursor += 2

		if isinstance(blocks[cursor], (_DecoratedFunction, _MultilineFunction)):
			# Add a blank line before a decorated function
			blocks.insert(cursor, [])
			cursor += 1

		if isinstance(blocks[cursor], _Class):

			if (
					cursor + 1 < len(blocks) and isinstance(blocks[cursor + 1], _Function)
					and not isinstance(blocks[cursor + 1], (_DecoratedFunction, _MultilineFunction))
					and blocks[cursor][-1].lstrip().startswith("class") and blocks[cursor + 1][0][0].isspace()
					):
				blocks.insert(cursor, [])
				cursor += 2
			else:
				blocks.insert(cursor, [])
				blocks.insert(cursor + 2, [])
				cursor += 3

		cursor += 1

	output = StringList()

	# Remove trailing whitespace from each block
	for block in blocks:
		if output and not block and not output[-1]:
			# Remove duplicate new lines
			continue

		output.append('\n'.join(block).rstrip())

	if not output[0]:
		output.pop(0)

	output.blankline(ensure_single=True)

	return output
