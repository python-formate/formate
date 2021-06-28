===============
Changelog
===============

Unreleased
-------------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.reformat_file` -- Only write to the file if there have been any changes.
  This avoids unnecessary changes to the mtime.


0.4.7
----------

Bugs Fixed
^^^^^^^^^^^^^

* :mod:`formate.reformat_generics` -- Correctly handle boolean values in Literals.


0.4.6
----------

Bugs Fixed
^^^^^^^^^^^^^

* :mod:`formate.dynamic_quotes` -- Preserve quote style in docstrings.


0.4.5
----------

Bugs Fixed
^^^^^^^^^^^^^

* :mod:`formate.config` -- The decorators now use a type variable to indicate to type checkers the returned object has the same type as the decorated object.
* :func:`formate.isort_hook` and :func:`formate.yapf_hook` -- Don't crash when keys are missing from ``formate_global_config`` and aren't in ``**kwargs``.


0.4.4
----------

Enhancements
^^^^^^^^^^^^^

* Switched to :mod:`dom_toml` for reading TOML files.
* Relaxed the yapf version requirement to allow 0.31.0 in addition to 0.30.0
* Relaxed the isort version requirement from ``isort<=5.6.4,>=5.5.2`` to ``isort<=5.9.0,>=5.5.2``


0.4.3
----------

* Switched to whey_ as the build backend.

.. _whey: https://whey.readthedocs.io/en/latest/

0.4.2
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.mini_hooks.squish_stubs` -- Ensure space between classes and functions is preserved in cases where there would be no space between the class and a method.


0.4.1
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.mini_hooks.squish_stubs` -- Don't crash due to accessing an out-of-range value from a list.


0.4.0
----------

Enhancements
^^^^^^^^^^^^^

* :func:`formate.mini_hooks.squish_stubs` -- Remove whitespace between the class definition and first single-line function.


0.3.2
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.mini_hooks.squish_stubs` -- Don't crash due to accessing an out-of-range value from a list.



0.3.1
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.isort_hook` -- Preserve aliases / re-exports (e.g. import foo as foo) in stub files,
  as these are necessary for type checkers to understand re-exports.



0.3.0
----------

Enhancements
^^^^^^^^^^^^^

* Add support for reading the configuration from a ``[tool.formate]`` table in ``pyproject.toml``.



0.2.5
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.mini_hooks.squish_stubs` -- Improve handling of stubs with multiple decorators and keyword-only arguments.



0.2.4
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.isort_hook` -- Correctly handle isort options which may be either a single value or a sequence of values.



0.2.3
----------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`formate.mini_hooks.squish_stubs` -- Correctly handle comments and docstrings at the very top of stub files.



0.2.0
----------

Additions
^^^^^^^^^^^^

* :deco:`formate.config.wants_filename`
* :func:`formate.mini_hooks.squish_stubs`



0.1.0
----------

Initial release.
