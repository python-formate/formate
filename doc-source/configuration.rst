==============
Configuration
==============

``formate`` is configured using the ``formate.toml`` file in the root of your project
(alongside ``setup.py``, ``tox.ini`` etc.).

The ``-c / --config-file`` option can be used to point to a file with a different name,
but at this time the file must be TOML and must have the same layout.
At this time, the configuration cannot be placed in other files such as ``pyproject.toml``.

The file uses the `TOML <https://github.com/toml-lang/toml>`_ syntax, built around a top-level mapping of two keys:


``hooks``
------------

This is a mapping of hook names to their settings. The values can be either:

* an integer, representing the priority of the hook.
* a mapping of the following:

	+ ``priority`` -- as above.
	+ ``args`` -- a list of positional arguments to pass to the hook function. Optional. Default ``()``.
	+ ``kwargs`` -- a mapping of keyword arguments to pass to the hook function. Optional. Default ``{}``.

The `TOML <https://github.com/toml-lang/toml>`__ syntax allows for the mapping to spread over multiple tables, like so:

.. code-block:: toml

	[hooks]
	reformat-generics = 40
	collections-import-rewrite = 20
	noqa-reformat = 60
	ellipsis-reformat = 70

	[hooks.isort]
	priority = 50

	[hooks.isort.kwargs]
	multi_line_output = 8
	use_parentheses = true
	remove_redundant_aliases = true


``config``
------------

This is a mapping of general configuration settings, which hooks can use as they please.
Common keys include ``indent``, indicating the type of indent to use, and ``line_length``,
indicating how long lines may be.

Example:

.. code-block:: toml

	[config]
	indent = "\t"
	line_length = 115