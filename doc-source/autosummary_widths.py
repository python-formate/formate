# Based on https://github.com/sphinx-doc/sphinx/blob/3.x/sphinx/ext/autosummary/__init__.py
#
# Copyright (c) 2007-2021 by the Sphinx team.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from itertools import chain
from typing import List, Tuple

# 3rd party
from docutils import nodes
from docutils.statemachine import StringList
from domdf_python_tools import stringlist
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.ext.autosummary import Autosummary, autosummary_table
from sphinx.util import rst
from sphinx.util.docutils import SphinxDirective, switch_source_input
from sphinx_toolbox import latex


class AutosummaryWidths(Autosummary):

	def get_table(self, items: List[Tuple[str, str, str, str]]) -> List[nodes.Node]:
		"""
		Generate a proper list of table nodes for autosummary:: directive.

		:param items: A a list produced by :meth:`~.get_items`.
		"""
		table_spec = addnodes.tabular_col_spec()
		# table_spec['spec'] = r'\Xx{1}{3}\Xx{2}{3}'
		# table_spec['spec'] = r'\Xx{3}{8}\Xx{5}{8}'
		# table_spec['spec'] = r'\Xx{7}{16}\Xx{9}{16}'

		widths = chain.from_iterable(getattr(self.state.document, "autosummary_widths", ((1, 2), (1, 2))))
		table_spec["spec"] = r'\Xx{{{}}}{{{}}}\Xx{{{}}}{{{}}}'.format(*widths)

		table = autosummary_table('')
		real_table = nodes.table('', classes=["longtable"])
		table.append(real_table)
		group = nodes.tgroup('', cols=2)
		real_table.append(group)
		group.append(nodes.colspec('', colwidth=10))
		group.append(nodes.colspec('', colwidth=90))
		body = nodes.tbody('')
		group.append(body)

		def append_row(*column_texts: str) -> None:
			row = nodes.row('')
			source, line = self.state_machine.get_source_and_line()
			for text in column_texts:
				node = nodes.paragraph('')
				vl = StringList()
				vl.append(text, "%s:%d:<autosummary>" % (source, line))
				with switch_source_input(self.state, vl):
					self.state.nested_parse(vl, 0, node)
					try:
						if isinstance(node[0], nodes.paragraph):
							node = node[0]
					except IndexError:
						pass
					row.append(nodes.entry('', node))
			body.append(row)

		for name, sig, summary, real_name in items:
			qualifier = "obj"
			if "nosignatures" not in self.options:
				col1 = ":{}:`{} <{}>`\\ {}".format(qualifier, name, real_name, rst.escape(sig).replace('(', "(​"))
			else:
				col1 = f":{qualifier}:`{name} <{real_name}>`"
			col2 = summary
			append_row(col1, col2)

		return [table_spec, table]


class WidthsDirective(SphinxDirective):
	required_arguments = 2

	def run(self):
		widths = [arg.split('/') for arg in self.arguments]
		self.state.document.autosummary_widths = widths
		return []


def configure(app: Sphinx, config: Config):
	"""

	:param app:
	:param config:
	"""

	latex_elements = getattr(app.config, "latex_elements", {})  # type: ignore

	latex_preamble = stringlist.StringList(latex_elements.get("preamble", ''))
	latex_preamble.blankline()
	latex_preamble.append(r"\makeatletter")
	latex_preamble.append(r"\newcolumntype{\Xx}[2]{>{\raggedright\arraybackslash}p{\dimexpr")
	latex_preamble.append(r"    (\linewidth-\arrayrulewidth)*#1/#2-\tw@\tabcolsep-\arrayrulewidth\relax}}")
	latex_preamble.append(r"\makeatother")
	latex_preamble.blankline()

	latex_elements["preamble"] = str(latex_preamble)
	app.config.latex_elements = latex_elements  # type: ignore


def setup(app: Sphinx):
	app.add_directive("autosummary", AutosummaryWidths, override=True)
	app.add_directive("autosummary-widths", WidthsDirective)
	app.connect("build-finished", latex.replace_unknown_unicode)
	app.connect("config-inited", configure)
