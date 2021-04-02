# 3rd party
import pytest
from coincidence.selectors import not_pypy
from testing_tox import run_tox


@pytest.fixture()
def basic_docs_testenv(tmp_pathplus):
	build_dir = tmp_pathplus / "doc-source" / "build"
	build_dir.mkdir(parents=True)

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:docs]",
			"deps = sphinx",
			"skip_install = True",
			"commands = sphinx-build --version",
			])

	return build_dir


def test_rmdir_docs(basic_docs_testenv, tmp_pathplus, capsys):
	with (tmp_pathplus / "tox.ini").open('a') as fp:
		fp.write('recreate_hook = builtin.rmdir(r"{toxinidir}/doc-source/build")\n')

	try:
		run_tox(["-e", "docs", "-r"], tmp_pathplus)
	finally:
		stdout = capsys.readouterr().out
		print(stdout)

	assert (tmp_pathplus / "doc-source").is_dir()
	assert not basic_docs_testenv.is_dir()

	assert f"docs recreate hook: removing {basic_docs_testenv}" in stdout


@not_pypy("mypy does noy support PyPy")
def test_rmdir_mypy(tmp_pathplus, capsys):

	cache_dir = tmp_pathplus / ".mypy_cache"
	cache_dir.mkdir()

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:mypy]",
			"deps = mypy",
			"skip_install = True",
			"commands = mypy --version",
			'recreate_hook = builtin.rmdir(r"{toxinidir}/.mypy_cache")',
			])

	try:
		run_tox(["-e", "mypy", "-r"], tmp_pathplus)
	finally:
		stdout = capsys.readouterr().out
		print(stdout)

	assert not cache_dir.is_dir()

	assert f"mypy recreate hook: removing {cache_dir}" in stdout


def test_simple_custom_hook(basic_docs_testenv, tmp_pathplus, capsys):
	with (tmp_pathplus / "tox.ini").open('a') as fp:
		fp.write('recreate_hook = "hello world"')

	try:
		run_tox(["-e", "docs", "-r"], tmp_pathplus)
	finally:
		stdout = capsys.readouterr().out
		print(stdout)

	assert f"docs recreate hook: hello world" in stdout


def test_custom_hook(basic_docs_testenv, tmp_pathplus, capsys):
	with (tmp_pathplus / "tox.ini").open('a') as fp:
		fp.write('recreate_hook = custom_hook.custom_hook()\n')

	(tmp_pathplus / "custom_hook.py").write_lines([
			"def custom_hook() -> str:",
			'\treturn "this is a custom hook"',
			])

	try:
		run_tox(["-e", "docs", "-r"], tmp_pathplus)
	finally:
		stdout = capsys.readouterr().out
		print(stdout)

	assert f"docs recreate hook: this is a custom hook" in stdout


def test_no_hook(basic_docs_testenv, tmp_pathplus, capsys):

	try:
		run_tox(["-e", "docs", "-r"], tmp_pathplus)

	finally:
		stdout = capsys.readouterr().out
		print(stdout)

	assert "docs recreate hook: " not in stdout


def test_not_recreate(basic_docs_testenv, tmp_pathplus, capsys):
	with (tmp_pathplus / "tox.ini").open('a') as fp:
		fp.write('recreate_hook = builtin.rmdir(r"{toxinidir}/doc-source/build")\n')

	try:
		run_tox(["-e", "docs"], tmp_pathplus)
	finally:
		stdout = capsys.readouterr().out
		print(stdout)

	assert (tmp_pathplus / "doc-source").is_dir()
	assert basic_docs_testenv.is_dir()

	assert "docs recreate hook: " not in stdout
