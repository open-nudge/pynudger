# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Module testing string rules violations."""

# noqa-file: PYNUDGER46

from __future__ import annotations


async def empty_return() -> str:
    """Return an empty string.

    Returns:
        Empty string value.

    """
    return ""
