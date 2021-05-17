#!/usr/bin/env python3
#
#  classes.py
"""
Core classes.

.. autosummary-widths:: 7/16 9/16
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
from typing import Any, Callable, Dict, Iterator, List, Mapping, Optional, Sequence, Union

# 3rd party
import attr
from attr_utils.pprinter import pretty_repr
from attr_utils.serialise import serde
from domdf_python_tools.typing import PathLike
from typing_extensions import TypedDict

__all__ = ["FormateConfigDict", "ExpandedHookDict", "HooksMapping", "EntryPoint", "Hook"]

#: Type hint for the ``hooks`` key of the ``formate`` configuration mapping.
HooksMapping = Mapping[str, Union[int, "ExpandedHookDict"]]


class FormateConfigDict(TypedDict, total=False):
	"""
	:class:`typing.TypedDict` representing the configuration mapping parsed from ``formate.toml`` or similar.
	"""

	hooks: HooksMapping
	"""
	Mapping defining the hooks to run.

	Each value can either be an integer (the priority) or a :class:`~.ExpandedHookDict`.
	"""

	#: Mapping defining the global configuration for ``formate``.
	config: Mapping[str, Any]


class _BaseExpandedHookDict(TypedDict, total=False):
	#: The positional arguments passed to the hook function.
	args: List[Any]

	#: The keyword arguments passed to the hook function.
	kwargs: Dict[str, Any]


class ExpandedHookDict(_BaseExpandedHookDict):
	"""
	:class:`typing.TypedDict` representing the expanded form of a hook
	in the mapping parsed from the config file.
	"""  # noqa: D400

	#: The priority of the hook.
	priority: int


@pretty_repr
@serde
@attr.s
class Hook:
	"""
	Represents a ``formate`` reformatting hook.

	.. autosummary-widths:: 6/16 10/16
	"""

	#: The name of the hook. The name is normalized into lowercase, with underscores replaced by hyphens.
	name: str = attr.ib()

	#: The priority of the hook.
	priority: int = attr.ib(default=10)

	#: The positional arguments passed to the hook function.
	args: Sequence[Any] = attr.ib(default=(), converter=tuple)

	#: The keyword arguments passed to the hook function.
	kwargs: Dict[str, Any] = attr.ib(default={})

	entry_point: Optional["EntryPoint"] = attr.ib(default=None)

	#: A read-only view on the global configuration mapping, for hooks to do with as they wish.
	global_config: Mapping[str, Any] = attr.ib(factory=dict)

	@name.validator
	def _normalize(self, attribute, value):
		# this package
		from formate.utils import _normalize_pattern

		self.name = _normalize_pattern.sub('-', value).lower()

	@classmethod
	def parse(cls, data: HooksMapping) -> Iterator["Hook"]:
		r"""
		Parse the given mapping into :class:`~.Hook`\s.

		:param data:
		"""

		for hook, hook_config in data.items():
			if isinstance(hook_config, int):
				yield cls(hook, priority=hook_config)
			else:
				yield cls(hook, **hook_config)

	def __call__(self, source: str, filename: PathLike) -> str:
		"""
		Call the hook.

		:param source: The source to reformat.
		:param filename: The name of the source file.

		:return: The reformatted source.

		:raises: :exc:`TypeError` if ``entry_point`` has not been set.

		.. versionchanged:: 0.2.0  Added the ``filename`` argument.
		"""

		if self.entry_point is None:
			raise TypeError(f"hook {self.name!r} has no entry point configured.")

		hook_func = self.entry_point.obj

		kwargs = self.kwargs.copy()

		if getattr(hook_func, "wants_global_config", False):
			kwargs["formate_global_config"] = self.global_config
		if getattr(hook_func, "wants_filename", False):
			kwargs["formate_filename"] = filename

		return hook_func(source, *self.args, **kwargs)


@serde
@attr.s
class EntryPoint:
	"""
	Represents an entry point for a hook.
	"""

	#: The name of the entry point. The name is normalized into lowercase, with underscores replaced by hyphens.
	name: str = attr.ib()

	#: The object the entry point refers to.
	obj: Callable[..., str] = attr.ib()

	@name.validator
	def _normalize(self, attribute, value):
		# this package
		from formate.utils import _normalize_pattern

		self.name = _normalize_pattern.sub('-', value).lower()

	@obj.validator
	def _validate_obj(self, attribute, value):
		if not callable(value):
			raise TypeError(f"Entry points must be callables (e.g. classes and functions), not {type(value)!r}.")


if EntryPoint.to_dict.__doc__ is not None:
	EntryPoint.to_dict.__doc__ += "\n\n:rtype:\n\n.. raw:: latex\n\n\t\\clearpage"
