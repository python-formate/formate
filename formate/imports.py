#!/usr/bin/env python3
#
#  imports.py
"""
Converts import statements.
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
import collections.abc
import re

# 3rd party
from domdf_python_tools.stringlist import DelimitedList

# this package
from formate.utils import Rewriter

__all__ = ["CollectionsABCRewriter", "rewrite_collections_abc_imports"]


class CollectionsABCRewriter(Rewriter):
	"""
	Identify deprecated :file:`from collections import {<abc>}` imports,
	and rewrite them as :file:`from collections.abc import {<abc>}`.

	:param source: The source to reformat.
	"""  # noqa: D400

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: D102
		if node.level != 0:
			# relative import
			return

		if node.module != "collections":
			return

		new_imports = []

		collections_abc_imports: DelimitedList[str] = DelimitedList()
		collections_imports: DelimitedList[str] = DelimitedList()

		name: ast.alias
		for name in node.names:
			if name.name in collections.abc.__all__:  # type: ignore
				collections_abc_imports.append(name.name)
			else:
				collections_imports.append(name.name)

		text_range = self.tokens.get_text_range(node)

		if collections_abc_imports:
			new_imports.append(f"from collections.abc import {collections_abc_imports:, }")
		if collections_imports:
			new_imports.append(f"from collections import {collections_imports:, }")

		indent = re.split("[A-Za-z]", self.source.split('\n')[node.lineno - 1])[0]

		rewritten_imports = [new_imports[0]]
		rewritten_imports.extend(indent + imp for imp in new_imports[1:])

		self.record_replacement(text_range, '\n'.join(rewritten_imports))


def rewrite_collections_abc_imports(source: str) -> str:
	"""
	Identify deprecated :file:`from collections import {<abc>}` imports,
	and rewrite them as :file:`from collections.abc import {<abc>}`.

	:param source: The source to reformat.

	:returns: The reformatted source.
	"""  # noqa: D400

	return CollectionsABCRewriter(source).rewrite()
