# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test internal definition rules violations."""

from __future__ import annotations


class _UnusedClass:  # pyright: ignore[reportUnusedClass]
    """Define an unused internal class."""


class Owner:
    """Own an unused internal method."""

    def _unused_method(self) -> None:
        """Define an unused internal method."""


def _five_function(value: int) -> int:
    """Recursive function not being ran anywhere outside.

    This function should fail as the references inside
    **should not** be counted.

    Args:
        value:
            Value to reduce.

    Returns:
        Reduced value.

    """
    if value >= 0:
        return _five_function(value // 10)
    return _five_function(value - 1)
