# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Module testing no accidental string rules violations."""

# noqa-file: PYNUDGER46

from __future__ import annotations


def not_empty_return() -> str:
    """Return a non-empty string.

    Returns:
        Non-empty string value.

    """
    return "value"
