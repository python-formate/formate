########
formate
########

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc

.. only:: html

	.. include:: _blurb.rst


.. start shields

.. only:: html

	.. list-table::
		:stub-columns: 1
		:widths: 10 90

		* - Docs
		  - |docs| |docs_check|
		* - Tests
		  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
		* - PyPI
		  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
		* - Anaconda
		  - |conda-version| |conda-platform|
		* - Activity
		  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
		* - QA
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: formate
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-formate/formate/badge.svg
		:target: https://dependency-dash.repo-helper.uk/github/python-formate/formate/
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: formate
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: formate
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: formate
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: formate
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/formate?logo=anaconda
		:target: https://anaconda.org/domdfcoding/formate
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/formate?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/formate
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.7.0
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2024
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: formate
		:downloads: month
		:alt: PyPI - Downloads

.. end shields


Definitions
--------------

for·​mate

Etymology 1
************

`formic <https://en.wiktionary.org/wiki/formic#English>`_ + `-ate <https://en.wiktionary.org/wiki/-ate#English>`_

**formate** (plural `formates <https://en.wiktionary.org/wiki/formates#English>`_)

    *n.* (`organic chemistry <https://en.wiktionary.org/wiki/organic_chemistry>`_) Any `salt <https://en.wiktionary.org/wiki/salt>`_ or `ester <https://en.wiktionary.org/wiki/ester>`_ of `formic acid <https://en.wiktionary.org/wiki/formic_acid>`_.


Etymology 2
************

Portmanteau of `format <https://en.wiktionary.org/wiki/format#English>`_ + `mate <https://en.wiktionary.org/wiki/mate#English>`_

**formate**

    *n.* (`programming <https://en.wiktionary.org/wiki/programming>`_) A :wikipedia:`Python <https://en.wikipedia.org/wiki/Python_(programming_language)>` `autoformatting <https://en.wiktionary.org/wiki/autoformatting>`_ tool.


Installation
---------------

.. start installation

.. installation:: formate
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation


Contents
-----------

.. html-section::


.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 2
	:caption: Documentation
	:glob:

	usage
	configuration
	hooks
	extending
	changelog
	Source
	license

.. toctree::
	:maxdepth: 3
	:caption: API Reference
	:glob:

	api/formate
	api/*

.. sidebar-links::
	:github:
	:pypi: formate

	Contributing Guide<https://contributing-to-formate.readthedocs.io>


.. sidebar-links::
	:caption: Links
	:github:
	:pypi: formate


.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <python-formate/formate>`

.. end links
