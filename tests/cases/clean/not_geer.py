# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Testing no accidental getters rule violations."""

from __future__ import annotations


class GerClass:
    """Dummy getter class."""


def ger_function() -> None:
    """Dummy getter function."""
