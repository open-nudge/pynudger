# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test a private module exposing its matching public function."""

from __future__ import annotations

_helper = 0


def files() -> None:
    """Expose the public object represented by the module."""
