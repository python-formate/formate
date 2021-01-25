#!/usr/bin/env python3
#
#  dynamic_quotes.py
r"""
Applies "dynamic quotes" to Python source code.

The rules are:

* Use double quotes ``"`` where possible.
* Use single quotes ``'`` for empty strings and single characters (``a``, ``\n`` etc.).
* Leave the quotes unchanged for multiline strings, f strings and raw strings.
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
import json
import re
import sys
from io import StringIO
from typing import List

# 3rd party
import asttokens  # type: ignore

__all__ = ["dynamic_quotes"]

# this package
from formate.utils import double_repr


class QuoteRewriter(ast.NodeVisitor):  # noqa: D101

	def __init__(self):
		super().__init__()
		self.string_nodes: List[ast.Str] = []

	if sys.version_info[:2] < (3, 8):  # pragma: no cover (py38+)

		def visit_Str(self, node: ast.Str) -> None:  # noqa: D102
			self.string_nodes.append(node)
	else:  # pragma: no cover (<py38)

		def visit_Constant(self, node: ast.Constant) -> None:  # noqa: D102
			if isinstance(node.value, str):
				self.string_nodes.append(node)
			else:
				self.generic_visit(node)

	def visit(self, node: ast.AST) -> List[ast.Str]:  # noqa: D102
		super().visit(node)
		return self.string_nodes


def dynamic_quotes(source: str) -> str:
	"""
	Reformats quotes in the given source, and returns the reformatted source.

	:param source: The source to reformat.

	:returns: The reformatted source.
	"""

	offset = 0
	buf = StringIO()
	visitor = QuoteRewriter()
	atok = asttokens.ASTTokens(source, parse=True)

	def key_func(value):
		return atok.get_text_range(value)[0]

	try:
		for string_node in sorted(visitor.visit(atok.tree), key=key_func):
			text_range = atok.get_text_range(string_node)

			if text_range == (0, 0):
				continue

			buf.write(source[offset:text_range[0]])

			if source[text_range[0]:text_range[1]] in {'""', "''"}:
				buf.write("''")
			elif not re.match("^[\"']", source[text_range[0]:text_range[1]]):
				buf.write(source[text_range[0]:text_range[1]])
			elif len(string_node.s) == 1:
				buf.write(repr(string_node.s))
			elif '\n' in source[text_range[0]:text_range[1]]:
				buf.write(source[text_range[0]:text_range[1]])
			elif '\n' in string_node.s or "\\n" in string_node.s:
				buf.write(source[text_range[0]:text_range[1]])
			else:
				buf.write(double_repr(string_node.s))

			offset = text_range[1]

		buf.write(source[offset:])

		return buf.getvalue()

	except NotImplementedError as e:  # pragma: no cover
		print(f"An error occurred: {e}")
		return source
