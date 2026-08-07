# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test allowed and out-of-scope module-name identifiers."""

from __future__ import annotations

not_same_name = 1
values = [1]


class NotRepetition:
    """Use the exact same module name."""

    read_not_same_name: int = 1


def not_repetition() -> None:
    """Use the exact module name."""


def repetitioner() -> None:
    """Use a non-token substring of the module name."""


def wrapper(values: list[int]) -> None:
    """Use repeated-looking names outside the module scope.

    Args:
        values:
            Values to iterate over.
    """
    read_not_same_name = values[0]
    for read_not_same_name in values:
        _ = read_not_same_name


for read_not_same_name in values:
    _ = read_not_same_name
