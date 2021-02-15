##################
tox-recreate-hook
##################

.. start short_desc

**(experimental) Allows hooks to be defined which are called when recreating a tox testenv.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/tox-recreate-hook/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/tox-recreate-hook/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/tox-recreate-hook/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/tox-recreate-hook/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/tox-recreate-hook/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/tox-recreate-hook/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/tox-recreate-hook/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/tox-recreate-hook/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/tox-recreate-hook/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/tox-recreate-hook/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/tox-recreate-hook/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/tox-recreate-hook/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/tox-recreate-hook?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/tox-recreate-hook
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/domdfcoding/tox-recreate-hook
	:target: https://github.com/domdfcoding/tox-recreate-hook/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/tox-recreate-hook
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/tox-recreate-hook/v0.0.0
	:target: https://github.com/domdfcoding/tox-recreate-hook/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/tox-recreate-hook
	:target: https://github.com/domdfcoding/tox-recreate-hook/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/tox-recreate-hook/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/tox-recreate-hook/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``tox-recreate-hook`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/domdfcoding/tox-recreate-hook

.. end installation


Example configuration

.. code-block:: ini

	[testenv:docs]
	setenv = SHOW_TODOS = 1
	basepython = python3.8
	changedir = {toxinidir}/doc-source
	deps =
	    -r{toxinidir}/requirements.txt
	    -r{toxinidir}/doc-source/requirements.txt
	commands = sphinx-build -M html . ./build {posargs}
	recreate_hook = builtin.rmdir("{toxinidir}/doc-source/build")
