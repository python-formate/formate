========
Usage
========

.. only:: latex

	.. include:: _blurb.rst


Command Line
---------------

.. program:: formate

.. click:: formate.__main__:main
	:prog: formate
	:nested: none



As a ``pre-commit`` hook
----------------------------

``formate`` can also be used as a `pre-commit <https://pre-commit.com/>`_ hook.
To do so, add the following to your
`.pre-commit-config.yaml <https://pre-commit.com/#2-add-a-pre-commit-configuration>`_ file:

.. pre-commit::
	:rev: 1.1.1
	:hooks: formate
	:args: --verbose

The ``args`` option can be used to provide the command line arguments shown above.
By default ``formate`` is run with ``--verbose --diff``
