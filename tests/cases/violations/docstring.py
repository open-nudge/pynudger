# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test docstring rule violations."""
# noqa-file: PYNUDGER43

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Iterator


def needs_args(*_: typing.Any) -> None:
    """Missing arguments section."""


def needs_yields() -> Iterator[int]:
    """Missing yields section."""
    yield 1


def needs_returns() -> int:
    """Missing returns section."""
    return 1
