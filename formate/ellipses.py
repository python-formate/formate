#!/usr/bin/env python3
#
#  ellipses.py
"""
Move ellipses (``...``) for type stubs onto the end of the stub definition.

	Before:

	.. code-block:: python

		def foo(value: str) -> int:
			...

	After:

	.. code-block:: python

		def foo(value: str) -> int: ...
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

# this package
from formate.utils import Rewriter

__all__ = ["EllipsisRewriter", "ellipsis_reformat"]


class EllipsisRewriter(Rewriter):
	"""
	Move ellipses (``...``) for type stubs onto the end of the stub definition.

	:param source: The source to reformat.
	"""

	def rewrite_ellipsis(
			self,
			node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef],
			) -> None:
		"""
		Responsible for the actual rewriting.
		"""

		if not node.body:
			return

		if not isinstance(node.body[0], ast.Expr):
			return

		if not isinstance(node.body[0].value, (ast.Constant, ast.Ellipsis)):
			return

		if sys.version_info < (3, 8):  # pragma: no cover (py38+)
			if not isinstance(node.body[0].value, ast.Ellipsis):
				return

		else:  # pragma: no cover (<py38)
			if not node.body[0].value.value is Ellipsis:
				return

		body_text_range = self.tokens.get_text_range(node)
		ellipsis_text_range = self.tokens.get_text_range(node.body[0])
		node_source = self.source[body_text_range[0]:ellipsis_text_range[1]]

		self.record_replacement(
				(body_text_range[0], ellipsis_text_range[1]),
				re.sub(r':[\n\s]+\.\.\.', ": ...", node_source),
				)

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: D102
		self.rewrite_ellipsis(node)
		self.generic_visit(node)

	def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: D102
		self.rewrite_ellipsis(node)
		self.generic_visit(node)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: D102
		self.rewrite_ellipsis(node)
		self.generic_visit(node)


def ellipsis_reformat(source: str) -> str:
	"""
	Move ellipses (``...``) for type stubs onto the end of the stub definition.

		Before:

		.. code-block:: python

			def foo(value: str) -> int:
				...

		After:

		.. code-block:: python

			def foo(value: str) -> int: ...

	:param source: The source to reformat.

	:return: The reformatted source.
	"""

	if "..." not in source:
		return source

	return EllipsisRewriter(source).rewrite()
