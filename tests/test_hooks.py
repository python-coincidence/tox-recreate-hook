# stdlib
import sys

# 3rd party
import pytest
import tox  # type: ignore
import tox.reporter  # type: ignore
from coincidence.selectors import not_pypy
from domdf_python_tools.paths import in_directory


def test_rmdir_docs(tmp_pathplus, capsys):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	build_dir = tmp_pathplus / "doc-source" / "build"

	build_dir.mkdir(parents=True)

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:docs]",
			"deps = sphinx",
			"skip_install = True",
			"commands = sphinx-build --version",
			'recreate_hook = builtin.rmdir("{toxinidir}/doc-source/build")',
			])

	with pytest.raises(SystemExit), in_directory(tmp_pathplus):
		tox.cmdline(["-e", "docs", "-r"])

	stdout = capsys.readouterr().out
	print(stdout)

	assert (tmp_pathplus / "doc-source").is_dir()
	assert not build_dir.is_dir()

	assert f"docs recreate hook: removing {build_dir}" in stdout


@not_pypy("mypy does noy support PyPy")
def test_rmdir_mypy(tmp_pathplus, capsys):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	cache_dir = tmp_pathplus / ".mypy_cache"

	cache_dir.mkdir()

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:mypy]",
			"deps = mypy",
			"skip_install = True",
			"commands = mypy --version",
			'recreate_hook = builtin.rmdir("{toxinidir}/.mypy_cache")',
			])

	with pytest.raises(SystemExit), in_directory(tmp_pathplus):
		tox.cmdline(["-e", "mypy", "-r"])

	stdout = capsys.readouterr().out
	print(stdout)

	assert not cache_dir.is_dir()

	assert f"mypy recreate hook: removing {cache_dir}" in stdout


def test_simple_custom_hook(tmp_pathplus, capsys):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:docs]",
			"deps = sphinx",
			"skip_install = True",
			"commands = sphinx-build --version",
			'recreate_hook = "hello world"',
			])

	with pytest.raises(SystemExit), in_directory(tmp_pathplus):
		tox.cmdline(["-e", "docs", "-r"])

	stdout = capsys.readouterr().out
	print(stdout)

	assert f"docs recreate hook: hello world" in stdout


def test_custom_hook(tmp_pathplus, capsys):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:docs]",
			"deps = sphinx",
			"skip_install = True",
			"commands = sphinx-build --version",
			"recreate_hook = custom_hook.custom_hook()",
			])

	(tmp_pathplus / "custom_hook.py").write_lines([
			"def custom_hook() -> str:",
			'\treturn "this is a custom hook"',
			])

	with pytest.raises(SystemExit), in_directory(tmp_pathplus):
		tox.cmdline(["-e", "docs", "-r"])

	stdout = capsys.readouterr().out
	print(stdout)

	assert f"docs recreate hook: this is a custom hook" in stdout


def test_no_hook(tmp_pathplus, capsys):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:docs]",
			"deps = sphinx",
			"skip_install = True",
			"commands = sphinx-build --version",
			])

	with pytest.raises(SystemExit), in_directory(tmp_pathplus):
		tox.cmdline(["-e", "docs", "-r"])

	stdout = capsys.readouterr().out
	print(stdout)

	assert "docs recreate hook: " not in stdout


def test_not_recreate(tmp_pathplus, capsys):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	build_dir = tmp_pathplus / "doc-source" / "build"

	build_dir.mkdir(parents=True)

	(tmp_pathplus / "tox.ini").write_lines([
			"[testenv:docs]",
			"deps = sphinx",
			"skip_install = True",
			"commands = sphinx-build --version",
			'recreate_hook = builtin.rmdir("{toxinidir}/doc-source/build")',
			])

	with pytest.raises(SystemExit), in_directory(tmp_pathplus):
		tox.cmdline(["-e", "docs"])

	stdout = capsys.readouterr().out
	print(stdout)

	assert (tmp_pathplus / "doc-source").is_dir()
	assert build_dir.is_dir()

	assert "docs recreate hook: " not in stdout
