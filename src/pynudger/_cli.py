# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger CLI entrypoint."""

from __future__ import annotations

import pathlib
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


def _files_default(
    config: dict[str, typing.Any], path: pathlib.Path | str | None = None
) -> Iterable[pathlib.Path]:
    """Default files to lint.

    Returns:
        All Python files in the current working directory and its
        subdirectories, excluding some well-known directories like
        `__pypackages__`.

    """
    ignores = set(
        config.get(
            "dir_ignores", ["__pypackages__", ".venv", ".git", "__pycache__"]
        )
    ) | set(config.get("extend_dir_ignores", []))

    # Both no covers were tested previously, too cumbersome
    # to test these explicitly

    if path is None:  # pragma: no cover
        path = pathlib.Path.cwd()

    path = pathlib.Path(path).resolve()

    for p in path.rglob("*.py"):
        if ignores.isdisjoint(p.parts):  # pragma: no cover
            yield p


def main(
    args: list[str] | None = None,
    path: pathlib.Path | str | None = None,
    include_codes: Iterable[int] | None = None,
    exclude_codes: Iterable[int] | None = None,
) -> None:
    """Run the CLI.

    Args:
        args:
            Command line arguments to parse (used mainly for testing).
        path:
            Directory to lint (default: current working directory).
        include_codes:
            Lint codes to include (overrides config).
        exclude_codes:
            Lint codes to exclude (overrides config).

    """
    config = loadfig.config(NAME.lower())

    lintkit.registry.inject("config", config)

    if include_codes is None:  # pragma: no cover
        include_codes = config.get("include_codes")
    if exclude_codes is None:  # pragma: no cover
        exclude_codes = config.get("exclude_codes")

    lintkit.cli.main(
        version=version(NAME),
        files_default=_files_default(config, path),
        files_help=(
            "Files to lint with pynudger (default: all Python files in cwd)"
        ),
        include_codes=include_codes,
        exclude_codes=exclude_codes,
        end_mode=config.get("end_mode", "all"),
        args=args,
        description="pynudger - opennudge Python linter",
    )
