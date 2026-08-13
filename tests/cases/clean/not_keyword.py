# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Tests no accidental keyword-based violations."""

# noqa-file: PYNUDGER46

from __future__ import annotations


def not_state() -> None:
    """Should not violate state rule 19 (del statement)."""


def iteration() -> None:
    """Should not violate iteration rule 20 (break statement)."""
    for _ in range(2):
        pass
