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
import os
import pathlib
import re
import sys
from contextlib import contextmanager
from itertools import starmap
from operator import itemgetter
from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple, TypeVar

# 3rd party
import asttokens
import click
from consolekit import terminal_colours
from consolekit.tracebacks import TracebackHandler
from domdf_python_tools.import_tools import discover_entry_points_by_name
from domdf_python_tools.typing import PathLike

# this package
from formate.classes import EntryPoint, Hook
from formate.exceptions import HookNotFoundError

if TYPE_CHECKING:
	# stdlib
	from typing import NoReturn

__all__ = ("import_entry_points", "normalize", "syntaxerror_for_file", "Rewriter", "SyntaxTracebackHandler")

_normalize_pattern = re.compile(r"[-_.]+")


def normalize(name: str) -> str:
	"""
	Normalize the given name into lowercase, with underscores replaced by hyphens.

	:param name: The hook name.
	"""

	# From PEP 503 (public domain).

	return _normalize_pattern.sub('-', name).lower()


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

	.. autosummary-widths:: 8/16
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

		assert self.tokens.tree is not None

	def rewrite(self) -> str:
		"""
		Rewrite the source and return the new source.

		:returns: The reformatted source.
		"""

		tree = self.tokens.tree
		assert tree is not None
		self.visit(tree)

		reformatted_source = self.source

		# Work from the bottom up
		for (start, end), replacement in sorted(self.replacements, key=itemgetter(0), reverse=True):
			source_before = reformatted_source[:start]
			source_after = reformatted_source[end:]
			reformatted_source = ''.join([source_before, replacement, source_after])

		return reformatted_source

	def record_replacement(self, text_range: Tuple[int, int], new_source: str) -> None:
		"""
		Record a region of text to be replaced.

		:param text_range: The region of text to be replaced.
		:param new_source: The new text for that region.
		"""

		self.replacements.append((text_range, new_source))


class SyntaxTracebackHandler(TracebackHandler):
	"""
	Subclass of :class:`consolekit.tracebacks.TracebackHandler` to additionally handle :exc:`SyntaxError`.
	"""

	def handle_SyntaxError(self, e: SyntaxError) -> "NoReturn":  # noqa: D102
		click.echo(terminal_colours.Fore.RED(f"Fatal: {e.__class__.__name__}: {e}"), err=True)
		sys.exit(126)

	def handle_HookNotFoundError(self, e: HookNotFoundError) -> "NoReturn":  # noqa: D102
		click.echo(terminal_colours.Fore.RED(f"Fatal: Hook not found: {e}"), err=True)
		sys.exit(126)


@contextmanager
def syntaxerror_for_file(filename: PathLike) -> Iterator:
	"""
	Context manager to catch :exc:`SyntaxError` and set its filename to ``filename``
	if the current filename is ``<unknown>``.

	This is useful for syntax errors raised when parsing source into an AST.

	:param filename:

	.. clearpage::
	"""  # noqa: D400

	try:
		yield
	except SyntaxError as e:
		if e.filename == "<unknown>":
			e.filename = os.fspath(filename)

		raise e


_P = TypeVar("_P", bound=pathlib.Path)


def _find_from_parents(path: _P) -> _P:
	"""
	Try to find ``path`` in the current directory or its parents.

	If the file can't be found ``path`` is returned.
	"""

	if len(path.parts) == 1 and not path.exists():
		for parent in path.cwd().parents:
			candidate = parent / path
			if candidate.exists():
				return candidate

	return path
