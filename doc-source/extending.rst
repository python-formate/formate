========================
Creating your own hooks
========================

It is easy to create your own hooks to extend ``formate``. A basic hook looks like this:

.. code-block:: python

	def make_upper(source: str) -> str:
		"""
		Make all the source uppercase.

		:param source: The source to reformat.

		:return: The reformatted source.
		"""

		return source.upper()


An entry point must be configured for the hook. For Setuptools:

.. code-block:: ini

	[options.entry_points]

	formate_hooks =
	make_upper=<import path>:make_upper

Hooks may also accept positional and/or keyword arguments, either named or with ``*args`` and ``**kwargs``:

.. code-block:: python

	def change_case(source: str, upper: bool = True) -> str:
		"""
		Change the case of the source.

		:param source: The source to reformat.
		:param upper: Makes the source uppercase.

		:return: The reformatted source.
		"""

		if upper:
			return source.upper()
		else:
			return source.lower()


Some hooks may require access the the global configuration dict (the ``[config]`` table in ``formate.toml``).
Hooks can request this by using the :deco:`formate.config.wants_global_config`` decorator,
which provides the configuration as the ``formate_global_config`` keyword argument:

.. code-block:: python

	def change_indents(source: str, formate_global_config: Optional[Mapping] = None) -> str:
		"""
		Change the indents of the source.

		:param source: The source to reformat.
		:param formate_global_config: The global configuration dictionary. Optional.

		:return: The reformatted source.
		"""

		if formate_global_config is None:
			formate_global_config = {}

		indent = formate_global_config.get("indent", "\t")

		return re.sub("(    |\t)", indent, source)