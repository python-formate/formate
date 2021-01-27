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

__all__ = ["noqa_reformat", "check_ast"]


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
	"""

	ast.parse(source)
	return source
