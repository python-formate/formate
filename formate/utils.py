#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
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
from itertools import starmap
from operator import itemgetter
from typing import Any, Callable, Dict, List, Optional, Tuple

# 3rd party
import asttokens  # type: ignore
from domdf_python_tools.compat import importlib_metadata

# this package
from formate.classes import EntryPoint, Hook
from formate.exceptions import HookNotFoundError

__all__ = ["Rewriter", "import_entry_points", "normalize"]

_normalize_pattern = re.compile(r"[-_.]+")


def normalize(name: str) -> str:
	"""
	Normalize the given name into lowercase, with underscores replaced by hyphens.

	From :pep:`503` (public domain).

	:param name: The hook name.
	"""

	return _normalize_pattern.sub('-', name).lower()


def discover_entry_points_by_name(
		group_name: str,
		name_match_func: Optional[Callable[[Any], bool]] = None,
		object_match_func: Optional[Callable[[Any], bool]] = None,
		) -> Dict[str, Any]:
	"""
	Returns a mapping of entry point names to the entry points in the given category,
	optionally filtered by ``match_func``.

	.. versionadded:: 2.5.0

	:param group_name: The entry point group name, e.g. ``'entry_points'``.
	:param name_match_func: Function taking the entry point name and returning :py:obj:`True`
		if the entry point is to be included in the output.
	:default name_match_func: :py:obj:`None`, which includes all entry points.
	:param object_match_func: Function taking an object and returning :py:obj:`True`
		if the object is to be included in the output.
	:default object_match_func: :py:obj:`None`, which includes all objects.

	:return: List of matching objects.
	"""  # noqa: D400

	matching_objects = {}

	for entry_point in importlib_metadata.entry_points().get(group_name, ()):

		if name_match_func is not None and not name_match_func(entry_point.name):
			continue

		entry_point_obj = entry_point.load()

		if object_match_func is not None and not object_match_func(entry_point_obj):
			continue

		matching_objects[entry_point.name] = entry_point_obj

	return matching_objects


def import_entry_points(hooks: List[Hook]) -> Dict[str, EntryPoint]:
	"""
	Given a list of hooks, import the corresponding entry point and
	return a mapping of entry point names to :class:`~.EntryPoint` objects.

	:param hooks:

	:raises: :exc:`~.HookNotFoundError` if no entry point can be found for a hook.
	"""  # noqa: D400

	hook_names = [hook.name for hook in hooks]

	def name_match_func(name: str) -> bool:
		return normalize(name) in hook_names

	entry_points = {
			normalize(k): v
			for k,
			v in {
					**discover_entry_points_by_name("formate_hooks", name_match_func=name_match_func),
					**discover_entry_points_by_name("formate-hooks", name_match_func=name_match_func),
					}.items()
			}

	for hook in hooks:
		if hook.name not in entry_points:
			raise HookNotFoundError(hook)

	return {e.name: e for e in (starmap(EntryPoint, entry_points.items()))}


class Rewriter(ast.NodeVisitor):
	"""
	ABC for rewriting Python source files from an AST and a token stream.
	"""

	#: The original source.
	source: str

	#: The tokenized source.
	tokens: asttokens.ASTTokens

	replacements: List[Tuple[Tuple[int, int], str]]
	"""
	The parts of code to replace.

	Each element comprises a tuple of ``(start char, end char)`` in :attr:`~.source`,
	and the new text to insert between these positions.
	"""

	def __init__(self, source: str):
		self.source = source
		self.tokens = asttokens.ASTTokens(source, parse=True)
		self.replacements: List[Tuple[Tuple[int, int], str]] = []

	def rewrite(self) -> str:
		"""
		Rewrite the source and return the new source.

		:returns: The reformatted source.
		"""

		self.visit(self.tokens.tree)

		reformatted_source = self.source

		# Work from the bottom up
		for (start, end), replacement in sorted(self.replacements, key=itemgetter(0), reverse=True):
			source_before = reformatted_source[:start]
			source_after = reformatted_source[end:]
			reformatted_source = ''.join([source_before, replacement, source_after])

		return reformatted_source

	def record_replacement(self, text_range: Tuple[int, int], new_source: str):
		"""
		Record a region of text to be replaced.

		:param text_range: The region of text to be replaced.
		:param new_source: The new text for that region.
		"""

		self.replacements.append((text_range, new_source))
