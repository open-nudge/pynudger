# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0
"""Test call rule violations."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Iterator


def compatibility() -> object:
    """Should violate compatibility call rule 20.

    Returns:
        Restricted compatibility object.

    """
    return object()


def interactive() -> None:
    """Should violate interactive call rule 21."""
    help()


def cast() -> int:
    """Should violate cast call rule 22.

    Returns:
        Cast integer value.

    """
    return typing.cast("int", 42)


def insecure() -> None:
    """Should violate insecure call rule 23."""
    _ = compile("print('Hello')", "test", "eval")


def iteration() -> Iterator[typing.Any]:
    """Should violate iteration call rule 24.

    Returns:
        Iterator from restricted call.

    """
    return iter([])


def attribute() -> dict[str, typing.Any]:
    """Should violate attribute call rule 25.

    Returns:
        Dictionary from restricted attribute call.

    """
    return globals()
