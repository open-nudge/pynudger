# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Testing 'common' rule violations."""

from __future__ import annotations


class SharedClass:
    """Dummy shared class."""


def shared_function() -> None:
    """Dummy shared function."""
