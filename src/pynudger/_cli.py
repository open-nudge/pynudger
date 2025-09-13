# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
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

# Import all rules to register them (side-effect)
from pynudger import (  # noqa: E402
    _rule,  # noqa: F401  # pyright: ignore[reportUnusedImport]
)


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
        version(NAME),
        files_default=pathlib.Path.cwd().rglob("*.py"),
        files_help=(
            "Files to lint with pynudger (default: all Python files in cwd)"
        ),
        include_codes=include_codes,
        exclude_codes=exclude_codes,
        end_mode=config.get("end_mode", "all"),
        args=args,
        description="pynudger - opennudge Python linter",
    )
