# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger CLI entrypoint."""

from __future__ import annotations

import typing

from importlib.metadata import version

import lintkit

if typing.TYPE_CHECKING:
    import pathlib

    from collections.abc import Iterable

NAME = "pynudger"
IGNORED_DIRECTORIES = frozenset(
    {"__pypackages__", ".venv", ".git", "__pycache__"}
)

lintkit.settings.name.tool = NAME
lintkit.settings.name.rule = NAME.upper()

# Import all rule modules to register lintkit rules (side effect).
from pynudger import rule as rule  # noqa: E402, PLC0414


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
    lintkit.cli.main(
        version=version(NAME),
        files_default=lintkit.cli.files.default.Recursive(
            suffix=".py",
            directory=path,
            ignore_directories=IGNORED_DIRECTORIES,
        ),
        files_reader=lintkit.cli.files.reader.Recursive(
            suffix=".py",
            ignore_directories=IGNORED_DIRECTORIES,
        ),
        files_help=(
            "Files to lint with pynudger (default: all Python files in cwd)"
        ),
        names=names,
        args=args,
        description="pynudger - opennudge Python linter",
    )
