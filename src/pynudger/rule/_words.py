# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared name splitting and repeated-word matching."""

from __future__ import annotations

import re

import lintkit


def pascal(value: str | lintkit.Value[str]) -> list[str]:
    """Split a PascalCase name into words.

    Args:
        value:
            Name written with PascalCase boundaries.

    Returns:
        Words separated by the same uppercase boundaries used by the
        PascalCase length rule.
    """
    if isinstance(value, lintkit.Value):
        unwrapped: str = value.__wrapped__
    else:
        unwrapped = value
    return re.sub(
        "([A-Z][a-z]+)",
        r" \1",
        re.sub(
            "([A-Z]+)",
            r" \1",
            unwrapped,  # pyright: ignore[reportUnknownArgumentType]
        ),
    ).split()


def snake(value: str | lintkit.Value[str]) -> list[str]:
    """Split a snake_case name into words.

    Args:
        value:
            Name written with snake_case boundaries.

    Returns:
        Words separated by underscores, with leading and dunder underscores
        handled in the same way as the snake_case length rule.
    """
    if value.startswith("__") and value.endswith("__"):
        return value[2:-2].split("_")
    if value.startswith("_"):
        return value[1:].split("_")
    return value.split("_")
