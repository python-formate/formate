########
formate
########

.. start short_desc

**Python formatting mate.**

.. end short_desc

``formate`` runs a series of user-selected hooks which reformat Python source files.
This can include `changing quote characters`_, `rewriting imports`_, and calling tools such as isort_ and yapf_.

See `the documentation`_ for more information.

.. _changing quote characters: https://formate.readthedocs.io/en/latest/hooks.html#dynamic-quotes
.. _rewriting imports: https://formate.readthedocs.io/en/latest/hooks.html#collections-import-rewrite
.. _isort: https://pycqa.github.io/isort/
.. _yapf: https://github.com/google/yapf
.. _the documentation: https://formate.readthedocs.io/en/latest/

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/formate/latest?logo=read-the-docs
	:target: https://formate.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/repo-helper/formate/workflows/Docs%20Check/badge.svg
	:target: https://github.com/repo-helper/formate/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/repo-helper/formate/workflows/Linux/badge.svg
	:target: https://github.com/repo-helper/formate/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/repo-helper/formate/workflows/Windows/badge.svg
	:target: https://github.com/repo-helper/formate/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/repo-helper/formate/workflows/macOS/badge.svg
	:target: https://github.com/repo-helper/formate/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/repo-helper/formate/workflows/Flake8/badge.svg
	:target: https://github.com/repo-helper/formate/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/repo-helper/formate/workflows/mypy/badge.svg
	:target: https://github.com/repo-helper/formate/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/repo-helper/formate/requirements.svg?branch=master
	:target: https://requires.io/github/repo-helper/formate/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/repo-helper/formate/master?logo=coveralls
	:target: https://coveralls.io/github/repo-helper/formate?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/repo-helper/formate?logo=codefactor
	:target: https://www.codefactor.io/repository/github/repo-helper/formate
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/formate
	:target: https://pypi.org/project/formate/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/formate?logo=python&logoColor=white
	:target: https://pypi.org/project/formate/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/formate
	:target: https://pypi.org/project/formate/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/formate
	:target: https://pypi.org/project/formate/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/repo-helper/formate
	:target: https://github.com/repo-helper/formate/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/repo-helper/formate
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/repo-helper/formate/v0.4.5
	:target: https://github.com/repo-helper/formate/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/repo-helper/formate
	:target: https://github.com/repo-helper/formate/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/formate
	:target: https://pypi.org/project/formate/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``formate`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install formate

.. end installation
