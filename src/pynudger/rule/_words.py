# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared name splitting and repeated-word matching."""

from __future__ import annotations

import re

import lintkit


def pascal(
    value: str | lintkit.Value[str],
    remove_suffix: str | None = None,
    exclude_word: str | None = None,
) -> list[str]:
    """Split a PascalCase name and optionally remove its final word.

    Args:
        value:
            Name written with PascalCase boundaries.
        remove_suffix:
            Final word to omit when it matches exactly.
        exclude_word:
            Complete word to omit without regard to case.

    Returns:
        Words separated by the same uppercase boundaries used by the
        PascalCase length rule, except an optional matching final word.
    """
    return _postprocess(
        re.sub(
            "([A-Z][a-z]+)",
            r" \1",
            re.sub(
                "([A-Z]+)",
                r" \1",
                _preprocess(value, remove_suffix),
            ),
        ).split(),
        exclude_word,
    )


def snake(
    value: str | lintkit.Value[str],
    remove_suffix: str | None = None,
    exclude_word: str | None = None,
) -> list[str]:
    """Split a snake_case name into words.

    Args:
        value:
            Name written with snake_case boundaries.
        remove_suffix:
            Final word to omit when it matches exactly.
        exclude_word:
            Complete word to omit without regard to case.

    Returns:
        Words separated by underscores, with leading and dunder underscores
        handled in the same way as the snake_case length rule.
    """
    name = _preprocess(value, remove_suffix)
    if name.startswith("__") and name.endswith("__"):
        words = name[2:-2].split("_")
    elif name.startswith("_"):
        words = name[1:].split("_")
    else:
        words = name.split("_")
    return _postprocess(words, exclude_word)


def _preprocess(value: str | lintkit.Value[str], suffix: str | None) -> str:
    """Unwrap a value and remove an optional suffix.

    Args:
        value:
            Plain string or lintkit value.
        suffix:
            Suffix to remove when present.

    Returns:
        The underlying string without the optional suffix.
    """
    unwrapped = value.__wrapped__ if isinstance(value, lintkit.Value) else value
    return unwrapped.removesuffix(suffix or "")


def _postprocess(words: list[str], exclude_word: str | None) -> list[str]:
    """Remove words matching the optional exclusion.

    Args:
        words:
            Split name words.
        exclude_word:
            Complete word to omit without regard to case.

    Returns:
        Words with the excluded word removed.
    """
    return [word for word in words if word.casefold() != exclude_word]
