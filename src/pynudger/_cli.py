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
from pynudger import _rule as _rule  # noqa: E402, PLC0414
from pynudger._restricted import rule as rule  # noqa: E402, PLC0414


def _files_default(config: dict[str, typing.Any]) -> Iterable[pathlib.Path]:
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

    for p in pathlib.Path.cwd().rglob("*.py"):
        if ignores.isdisjoint(p.parts):
            yield p


def main(
    args: list[str] | None = None,
    include_codes: Iterable[int] | None = None,
    exclude_codes: Iterable[int] | None = None,
) -> None:
    """Run the CLI."""
    config = loadfig.config(NAME.lower())

    lintkit.registry.inject("config", config)

    if include_codes is None:  # pragma: no cover
        include_codes = config.get("include_codes")
    if exclude_codes is None:  # pragma: no cover
        exclude_codes = config.get("exclude_codes")

    lintkit.cli.main(
        version=version(NAME),
        files_default=_files_default(config),
        files_help=(
            "Files to lint with pynudger (default: all Python files in cwd)"
        ),
        include_codes=include_codes,
        exclude_codes=exclude_codes,
        end_mode=config.get("end_mode", "all"),
        args=args,
        description="pynudger - opennudge Python linter",
    )
