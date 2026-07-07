# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0
"""Test no accidental call rule violations."""

from __future__ import annotations


def not_compatibility() -> None:
    """Should not violate compatibility call rule 20."""


def not_interactive() -> None:
    """Should not violate interactive call rule 21."""


def cast() -> None:
    """Should not violate cast call rule 22."""


def insecure() -> None:
    """Should not violate insecure call rule 23."""


def iteration() -> None:
    """Should not violate iteration call rule 24."""


def attribute() -> None:
    """Should not violate attribute call rule 25."""
