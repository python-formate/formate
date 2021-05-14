==============
Built-in Hooks
==============

``formate`` ships with several hooks out of the box:

.. _dynamic_quotes:

``dynamic_quotes``
--------------------

Reformats quotes in the given source, and returns the reformatted source.

This hook takes no arguments.


.. _collections-import-rewrite:

``collections-import-rewrite``
---------------------------------

.. raw:: latex

	\begin{flushleft}

Identify deprecated :file:`from collections import {<abc>}` imports,
and rewrite them as :file:`from collections.abc import {<abc>}`.

.. raw:: latex

	\end{flushleft}

This hook takes no arguments.


.. _noqa_reformat:

``noqa_reformat``
--------------------

Pull ``# noqa: ...`` comments that immediately follow docstrings back up to the end of the correct line.

This hook takes no arguments.


.. _check_ast:

``check_ast``
--------------------

Check the source can be parsed as a Python Abstract Syntax Tree.
This could be called early in the execution -- to check the file is valid before starting reformatting -- and again at the end to ensure no errors were introduced by the reformatting.

This hook takes no arguments.


.. _squish_stubs:

``squish_stubs``
--------------------

Squash type stubs by removing unnecessary blank lines.

This hook takes no arguments.


.. _ellipsis_reformat:

``ellipsis_reformat``
-----------------------

Move ellipses (``...``) for type stubs onto the end of the stub definition.

	Before:

	.. code-block:: python

		def foo(value: str) -> int:
			...

	After:

	.. code-block:: python

		def foo(value: str) -> int: ...

This hook takes no arguments.


.. _reformat-generics:

``reformat-generics``
----------------------

Reformats generics (:class:`typing.Generic`, :py:obj:`typing.Union`, :py:obj:`typing.Callable` etc.).

This hook takes a single keyword argument: ``indent``.
The indent can also be configured via the ``indent`` key in the :ref:`config <formate_toml_config>` table.


.. _isort:

``isort``
-----------

Calls `isort <https://pypi.org/project/isort/>`__, using the given keyword arguments as its configuration.

This hook only takes keyword arguments.

The max line length can be provided via the ``line_length`` keyword argument
or in the :ref:`config <formate_toml_config>` table as ``line_length``.


.. _yapf:

``yapf``
-----------

Calls `yapf <https://github.com/google/yapf>`__, using the given keyword arguments as its configuration.

This hook only takes keyword arguments.

The indent can be configured via the ``use_tabs`` keyword argument
or in the :ref:`config <formate_toml_config>` table as ``indent``.
