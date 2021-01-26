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
import re
import sys
from typing import Union

# 3rd party
from domdf_python_tools.utils import double_repr_string

# this package
from formate.utils import Rewriter

__all__ = ["dynamic_quotes"]


class QuoteRewriter(Rewriter):  # noqa: D101

	if sys.version_info[:2] < (3, 8):  # pragma: no cover (py38+)

		def visit_Str(self, node: ast.Str) -> None:  # noqa: D102
			self.rewrite_quotes_for_node(node)
	else:  # pragma: no cover (<py38)

		def visit_Constant(self, node: ast.Constant) -> None:  # noqa: D102
			if isinstance(node.value, str):
				self.rewrite_quotes_for_node(node)
			else:
				self.generic_visit(node)

	def rewrite_quotes_for_node(self, node: Union[ast.Str, ast.Constant]):
		text_range = self.tokens.get_text_range(node)

		if text_range == (0, 0):
			return

		string = self.source[text_range[0]:text_range[1]]

		if string in {'""', "''"}:
			self.record_replacement(text_range, "''")
		elif not re.match("^[\"']", string):
			return
		elif len(node.s) == 1:
			self.record_replacement(text_range, repr(node.s))
		elif '\n' in string:
			return
		elif '\n' in node.s or "\\n" in node.s:
			return
		else:
			self.record_replacement(text_range, double_repr_string(node.s))


def dynamic_quotes(source: str) -> str:
	"""
	Reformats quotes in the given source, and returns the reformatted source.

	:param source: The source to reformat.

	:returns: The reformatted source.
	"""

	return QuoteRewriter(source).rewrite()
