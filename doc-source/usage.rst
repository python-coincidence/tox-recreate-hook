=========
Usage
=========

``tox-recreate-hook`` is configured using the ``recreate_hook`` key in the ``testenv`` sections of ``tox.ini``.
The configuration might look like:

.. code-block:: ini

	[tox]
	envlist = py37, py38, py39, mypy, docs
	skip_missing_interpreters = True
	isolated_build = True
	requires =
	    pip>=21
	    tox-recreate-hook

	[testenv:docs]
	changedir = {toxinidir}/doc-source
	deps = -r{toxinidir}/doc-source/requirements.txt
	commands = sphinx-build -M html . ./build {posargs}
	recreate_hook = builtin.rmdir("{toxinidir}/doc-source/build")

``recreate_hook`` can be any valid single-line Python expression, the result of which will be printed to the terminal. ``tox-recreate-hook`` ships with :ref:`several hooks <builtin_hooks>` in the ``builtin`` module. Hooks can also be defined in custom modules, either on the :envvar:`PYTHONPATH` or in :any:`toxinidir`.
