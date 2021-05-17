#!/usr/bin/env python3
#
#  __init__.py
"""
Python formatting mate.
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
from configparser import ConfigParser
from typing import Iterable, Mapping, Optional, Sequence

# 3rd party
import click
import isort
from consolekit.terminal_colours import ColourTrilean, resolve_color_default
from consolekit.utils import coloured_diff
from domdf_python_tools.paths import PathPlus, TemporaryPathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike
from domdf_python_tools.words import TAB
from isort.exceptions import FileSkipComment

# this package
from formate.classes import FormateConfigDict, Hook
from formate.config import parse_hooks, wants_filename, wants_global_config
from formate.utils import syntaxerror_for_file

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.4.5"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["call_hooks", "reformat_file", "Reformatter", "isort_hook", "yapf_hook"]

# TODO: Ideas for hooks
# * https://github.com/asottile/add-trailing-comma
# * Replace collections imports with their typing equivalents where possible.
# * nested with block reformat, dependent on linelength
# * replace typing imports with typing_extensions where necessary. Needs min version flag
# * replace e.g `import numpy as np` with `import numpy` and update all usages
# * replace wildcard import with the things what is imported
# * replace `exit()` with `sys.exit()` and add import if required


def call_hooks(hooks: Iterable[Hook], source: str, filename: PathLike) -> str:
	"""
	Given a list of hooks (in order), call them in turn to reformat the source.

	:param hooks:
	:param source: The source to reformat.
	:param filename: The name of the source file.

	:returns: The reformatted source.

	.. versionchanged:: 0.4.3  Added the ``filename`` argument.
	"""

	for hook in hooks:
		source = hook(source, filename)

	return source


isort_string_or_sequence = {
		"skip",
		"skip_glob",
		"sections",
		"known_future_library",
		"known_third_party",
		"known_first_party",
		"known_local_folder",
		"known_standard_library",
		"extra_standard_library",
		"forced_separate",
		"length_sort_sections",
		"add_imports",
		"remove_imports",
		"single_line_exclusions",
		"no_lines_before",
		"sources",
		"src_paths",
		"treat_comments_as_code",
		"supported_extensions",
		"blocked_extensions",
		"constants",
		"classes",
		"variables",
		"namespace_packages",
		}
# TODO: known_other, dict


@wants_filename
@wants_global_config
def isort_hook(
		source: str,
		formate_filename: PathLike,
		formate_global_config: Optional[Mapping] = None,
		**kwargs,
		) -> str:
	r"""
	Call `isort <https://pypi.org/project/isort/>`_, using the given keyword arguments as its configuration.

	:param source: The source to reformat.
	:param formate_filename: The path to the file being reformatted.
	:param formate_global_config: The global configuration dictionary. Optional.
	:param \*\*kwargs:

	:returns: The reformatted source.
	"""

	if "isort_config_file" in kwargs:
		isort_config = isort.Config(settings_file=str(kwargs["isort_config_file"]))
	else:
		if "line_length" not in kwargs and formate_global_config:
			if "line_length" in (formate_global_config or {}):
				kwargs["line_length"] = formate_global_config["line_length"]

		parsed_kwargs = {}
		import_headings = {}

		for option, value in kwargs.items():
			if option.startswith("import_heading"):
				import_headings[option[len("import_heading") + 1:]] = value
			elif option in isort_string_or_sequence:
				if isinstance(value, str):
					value = (value, )
				elif not isinstance(value, Sequence):
					value = (value, )

				parsed_kwargs[option] = value

			elif option == "force_to_top":
				continue  # TODO isort expects a frozenset but I thought it was boolean?
			elif option == "remove_redundant_aliases":
				continue
			else:
				parsed_kwargs[option] = value

		isort_config = isort.Config(import_headings=import_headings, **parsed_kwargs)

	if PathPlus(formate_filename).suffix == ".pyi":
		object.__setattr__(isort_config, "remove_redundant_aliases", False)

	try:
		return isort.code(source, config=isort_config)
	except FileSkipComment:
		return source


@wants_global_config
def yapf_hook(source: str, formate_global_config: Optional[Mapping] = None, **kwargs) -> str:
	r"""
	Call `yapf <https://github.com/google/yapf>`_, using the given keyword arguments as its configuration.

	:param source: The source to reformat.
	:param formate_global_config: The global configuration dictionary. Optional.
	:param \*\*kwargs:

	:returns: The reformatted source.
	"""

	# 3rd party
	from yapf.yapflib.yapf_api import FormatCode  # type: ignore

	if "yapf_style" in kwargs:
		return FormatCode(source, style_config=str(kwargs["yapf_style"]))[0]

	else:
		if "use_tabs" not in kwargs and formate_global_config:
			if "indent" in (formate_global_config or {}):
				kwargs["use_tabs"] = formate_global_config["indent"] == TAB

		if "column_limit" not in kwargs and formate_global_config:
			if "line_length" in (formate_global_config or {}):
				kwargs["column_limit"] = formate_global_config["line_length"]

		with TemporaryPathPlus() as tmpdir:
			config_file = tmpdir / ".style.yapf"

			config = ConfigParser()
			config.read_dict({"style": kwargs})

			with config_file.open('w') as fp:
				config.write(fp)

			return FormatCode(source, style_config=str(config_file))[0]


class Reformatter:
	"""
	Reformat a Python source file.

	:param filename: The filename to reformat.
	:param config: The ``formate`` configuration, parsed from a TOML file (or similar).

	.. autosummary-widths:: 5/16 11/16
	"""

	#: The filename being reformatted.
	filename: str

	#: The filename being reformatted, as a POSIX-style path.
	file_to_format: PathPlus

	#: The ``formate`` configuration, parsed from a TOML file (or similar).
	config: FormateConfigDict

	def __init__(self, filename: PathLike, config: FormateConfigDict):
		self.file_to_format = PathPlus(filename)
		self.filename = self.file_to_format.as_posix()
		self.config = config
		self._unformatted_source = self.file_to_format.read_text()
		self._reformatted_source: Optional[str] = None

	def run(self) -> bool:
		"""
		Run the reformatter.

		:return: Whether the file was changed.
		"""

		hooks = parse_hooks(self.config)
		reformatted_source = StringList(call_hooks(hooks, self._unformatted_source, self.filename))
		reformatted_source.blankline(ensure_single=True)

		self._reformatted_source = str(reformatted_source)

		return self._reformatted_source != self._unformatted_source

	def get_diff(self) -> str:
		"""
		Returns the diff between the original and reformatted file content.
		"""

		# Based on yapf
		# Apache 2.0 License

		after = self.to_string().split('\n')
		before = self._unformatted_source.split('\n')
		return coloured_diff(
				before,
				after,
				self.filename,
				self.filename,
				"(original)",
				"(reformatted)",
				lineterm='',
				)

	def to_string(self) -> str:
		"""
		Return the reformatted file as a string.

		:rtype:

		.. latex:clearpage::
		"""

		if self._reformatted_source is None:
			raise ValueError("'Reformatter.run()' must be called first!")

		return self._reformatted_source

	def to_file(self) -> None:
		"""
		Write the reformatted source to the original file.
		"""

		self.file_to_format.write_text(self.to_string())


def reformat_file(
		filename: PathLike,
		config: FormateConfigDict,
		colour: ColourTrilean = None,
		):
	"""
	Reformat the given file, and show the diff if changes were made.

	:param filename: The filename to reformat.
	:param config: The ``formate`` configuration, parsed from a TOML file (or similar).
	:param colour: Whether to force coloured output on (:py:obj:`True`) or off (:py:obj:`False`).

	.. latex:clearpage::
	"""

	r = Reformatter(filename, config)

	with syntaxerror_for_file(filename):
		ret = r.run()

	if ret:
		click.echo(r.get_diff(), color=resolve_color_default(colour))

	r.to_file()

	return ret
