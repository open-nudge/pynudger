# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for keyword-based violations."""

# noqa-file: PYNUDGER46

from __future__ import annotations


def state() -> None:
    """Should violate state rule 19 (del statement)."""
    value = 1
    del value


def iteration() -> None:
    """Should violate iteration rule 20 (break statement)."""
    for _ in range(2):
        break
