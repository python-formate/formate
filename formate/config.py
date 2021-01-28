#!/usr/bin/env python3
#
#  config.py
"""
Read and parse formate configuration.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from operator import attrgetter
from types import MappingProxyType
from typing import Callable, List, Mapping, cast

# 3rd party
import toml
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from formate.classes import FormateConfigDict, Hook
from formate.utils import import_entry_points

__all__ = ["parse_hooks", "parse_global_config", "load_toml", "wants_global_config", "wants_filename"]


def parse_hooks(config: Mapping) -> List[Hook]:
	"""
	Given a mapping parsed from a TOML file (or similar), return a list of hooks selected by the user.

	:param config: The ``formate`` configuration, parsed from a TOML file (or similar).
	"""

	hooks = list(Hook.parse(config["hooks"]))
	entry_points = import_entry_points(hooks)
	global_config = parse_global_config(config)

	for hook in hooks:
		hook.entry_point = entry_points[hook.name]
		hook.global_config = global_config

	hooks = sorted(hooks, key=attrgetter("priority"))

	return hooks


def parse_global_config(config: Mapping) -> MappingProxyType:
	"""
	Returns a read-only view on the global configuration mapping, for hooks to do with as they wish.

	:param config: The ``formate`` configuration, parsed from a TOML file (or similar).
	"""

	return MappingProxyType(config.get("config", {}))


def load_toml(filename: PathLike) -> FormateConfigDict:
	"""
	Load the ``formate`` configuration mapping from the given TOML file.

	:param filename:
	"""

	return cast(FormateConfigDict, toml.loads(PathPlus(filename).read_text()))


def wants_global_config(func: Callable[..., str]) -> Callable[..., str]:
	"""
	Decorator to indicate to ``formate`` that the global configuration should be passed to this hook.

	The configuration will be provided as the ``formate_global_config``: :class:`~typing.Mapping` keyword argument.

	:param func:
	"""

	func.wants_global_config = True  # type: ignore
	return func


def wants_filename(func: Callable[..., str]) -> Callable[..., str]:
	"""
	Decorator to indicate to ``formate`` that the filename being reformatted should be passed to this hook.

	The configuration will be provided as the
	``formate_filename``: :class:`~domdf_python_tools.typing.PathLike` keyword argument.

	.. versionadded:: 0.2.0

	:param func:
	"""

	func.wants_filename = True  # type: ignore
	return func
