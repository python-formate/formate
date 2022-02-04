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
from typing import Mapping, Union

# 3rd party
from domdf_python_tools.utils import double_repr_string

# this package
from formate.utils import Rewriter

__all__ = ["dynamic_quotes"]


class QuoteRewriter(Rewriter):

	if sys.version_info[:2] < (3, 8):  # pragma: no cover (py38+)

		def visit_Str(self, node: ast.Str) -> None:
			self.rewrite_quotes_for_node(node)
	else:  # pragma: no cover (<py38)

		def visit_Constant(self, node: ast.Constant) -> None:
			if isinstance(node.value, str):
				self.rewrite_quotes_for_node(node)
			else:
				self.generic_visit(node)

	def visit_definition(self, node: Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
		"""
		Mark the docstring of the function or class to identify it later.

		:param node:
		"""

		if node.body and isinstance(node.body[0], ast.Expr):
			doc_node = node.body[0].value
			doc_node.is_docstring = True  # type: ignore

		self.generic_visit(node)

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		self.visit_definition(node)

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
		self.visit_definition(node)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
		self.visit_definition(node)

	def rewrite_quotes_for_node(self, node: Union[ast.Str, ast.Constant]) -> None:
		"""
		Mark the area for rewriting quotes in the given node.

		:param node:
		"""

		text_range = self.tokens.get_text_range(node)

		if text_range == (0, 0):
			return

		string = self.source[text_range[0]:text_range[1]]

		if getattr(node, "is_docstring", False):
			# TODO: format docstring with triple quotes and correct indentation
			return
		else:
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
				self.record_replacement(
						text_range,
						double_repr_string(node.s).translate(_surrogate_translator),
						)


def dynamic_quotes(source: str) -> str:
	"""
	Reformats quotes in the given source, and returns the reformatted source.

	:param source: The source to reformat.

	:returns: The reformatted source.
	"""

	return QuoteRewriter(source).rewrite()


class _LazyTranslate(Mapping):
	"""
	Escapes surrogates in the range U+D800 to U+DFFF, so they are left unchanged in the source.
	"""

	def __iter__(self):
		raise NotImplementedError

	def __len__(self):
		raise NotImplementedError

	def __getitem__(self, item: int) -> str:
		if item in range(55296, 57343):
			return repr(chr(item)).strip("'")
		else:
			return chr(item)


_surrogate_translator = _LazyTranslate()
