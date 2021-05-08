# 3rd party
from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.writers.latex import LaTeXTranslator

commands = r"""
\makeatletter
  \renewcommand{\DOCH}{%
    \mghrulefill{\RW}\par\nobreak
    \CNV\FmN{\@chapapp}\par\nobreak
    \CNoV\TheAlphaChapter\par\nobreak
    \vskip -1\baselineskip\vskip 5pt\mghrulefill{\RW}\par\nobreak
    \vskip 10\p@
    }
  \renewcommand{\DOTI}[1]{%
    \CTV\FmTi{#1}\par\nobreak
    \vskip 20\p@
    }
  \renewcommand{\DOTIS}[1]{%
    \CTV\FmTi{#1}\par\nobreak
    \vskip 20\p@
    }
\makeatother
"""


def visit_desc(translator: LaTeXTranslator, node: addnodes.desc) -> None:
	translator.body.append('\n\n\\vspace{5px}\n\n\\begin{fulllineitems}\n')
	if translator.table:
		translator.table.has_problematic = True


def depart_desc(translator: LaTeXTranslator, node: addnodes.desc) -> None:
	translator.body.append('\n\\end{fulllineitems}\n\n')


def visit_field_list(translator: LaTeXTranslator, node: nodes.field_list) -> None:
	translator.body.append('\\vspace{10px}\\begin{flushleft}\\begin{description}\n')
	if translator.table:
		translator.table.has_problematic = True


def depart_field_list(translator: LaTeXTranslator, node: nodes.field_list) -> None:
	translator.body.append('\\end{description}\\end{flushleft}\\vspace{10px}\n')


def configure(app: Sphinx, config: Config):
	"""
	Configure :mod:`sphinx_toolbox.tweaks.latex_toc`.

	:param app: The Sphinx application.
	:param config:
	"""

	if not hasattr(config, "latex_elements") or not config.latex_elements:  # pragma: no cover
		config.latex_elements = {}  # type: ignore

	latex_preamble = config.latex_elements.get("preamble", '')

	if commands not in latex_preamble:
		config.latex_elements["preamble"] = f"{latex_preamble}\n{commands}"


def setup(app: Sphinx):
	app.connect("config-inited", configure)
	app.add_node(addnodes.desc, latex=(visit_desc, depart_desc), override=True)
	app.add_node(nodes.field_list, latex=(visit_field_list, depart_field_list), override=True)
