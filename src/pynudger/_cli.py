# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger CLI entrypoint."""

from __future__ import annotations

import pathlib
import sys
import typing

from importlib.metadata import version

import lintkit
import loadfig

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

NAME = "pynudger"

lintkit.settings.name = NAME.upper()

# Import all rule modules to register lintkit rules (side effect).
from pynudger import rule as rule  # noqa: E402, PLC0414


def _files(
    config: dict[str, typing.Any],
    paths: Iterable[pathlib.Path | str],
) -> Iterable[pathlib.Path]:
    """Expand files and directories into a unique sequence of files.

    Args:
        config:
            Pynudger configuration containing directory ignore settings.
        paths:
            Files and directories to expand in their given order.

    Yields:
        Explicit files and Python files found recursively in directories,
        deduplicated by their resolved paths.

    """
    ignores = set(
        config.get(
            "dir_ignores", ["__pypackages__", ".venv", ".git", "__pycache__"]
        )
    ) | set(config.get("extend_dir_ignores", []))

    seen: set[pathlib.Path] = set()
    for path in paths:
        resolved = pathlib.Path(path).resolve()
        directory = resolved.is_dir()
        candidates = resolved.rglob("*.py") if directory else (resolved,)

        for candidate in candidates:
            canonical = candidate.resolve()
            if not (  # pragma: no branch
                (directory and not ignores.isdisjoint(canonical.parts))
                or canonical in seen
            ):
                seen.add(canonical)
                yield canonical


def _files_default(
    config: dict[str, typing.Any], path: pathlib.Path | str | None = None
) -> Iterable[pathlib.Path]:
    """Find the default files to lint.

    Args:
        config:
            Pynudger configuration containing directory ignore settings.
        path:
            Directory to search, or the current working directory by default.

    Returns:
        Python files below the selected directory, excluding ignored
        directories.

    """
    return _files(config, (pathlib.Path.cwd() if path is None else path,))


def main(
    args: list[str] | None = None,
    path: pathlib.Path | str | None = None,
    names: Iterable[str] | None = None,
) -> None:
    """Run the CLI.

    Args:
        args:
            Command line arguments to parse (used mainly for testing).
        path:
            Directory to lint (default: current working directory).
        names:
            Full, case-sensitive rule names to select (overrides config).

    """
    config = loadfig.config(NAME.lower())

    lintkit.registry.inject("config", config)

    if names is None:  # pragma: no cover
        names = config.get("names")

    selected_args = sys.argv[1:] if args is None else args
    if selected_args[:1] == ["check"]:
        selected_args = [
            "check",
            *(str(file) for file in _files(config, selected_args[1:])),
        ]

    lintkit.cli.main(
        version=version(NAME),
        files_default=_files_default(config, path),
        files_help=(
            "Files to lint with pynudger (default: all Python files in cwd)"
        ),
        names=names,
        end_mode=config.get("end_mode", "all"),
        args=selected_args,
        description="pynudger - opennudge Python linter",
    )
