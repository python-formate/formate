==============
Built-in Hooks
==============

``formate`` ships with several hooks out of the box:


``dynamic_quotes``
--------------------

Reformats quotes in the given source, and returns the reformatted source.

This hook takes no arguments.


``collections-import-rewrite``
---------------------------------

Identify deprecated :file:`from collections import {<abc>}` imports,
and rewrite them as :file:`from collections.abc import {<abc>}`.

This hook takes no arguments.


``noqa_reformat``
--------------------

Pull ``# noqa: ...`` comments that immediately follow docstrings back up to the end of the correct line.

This hook takes no arguments.


``check_ast``
--------------------

Check the source can be parsed as a Python Abstract Syntax Tree.
This could be called early in the execution -- to check the file is valid before starting reformatting -- and again at the end to ensure no errors were introduced by the reformatting.

This hook takes no arguments.


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


``reformat-generics``
----------------------

Reformats generics (:class:`typing.Generic`, :py:obj:`typing.Union`, :py:obj:`typing.Callable` etc.).

This hook takes no arguments.


``isort``
-----------

Calls `isort <https://pypi.org/project/isort/>`_, using the given keyword arguments as its configuration.

This hook only takes keyword arguments.


``yapf``
-----------

Calls `yapf <https://github.com/google/yapf>`_, using the given keyword arguments as its configuration.

This hook only takes keyword arguments.
