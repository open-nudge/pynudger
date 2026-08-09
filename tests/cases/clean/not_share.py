# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Testing no accidental 'shared' rule violations."""
# noqa-file: PYNUDGER43

from __future__ import annotations


class ShareClass:
    """Dummy not shared class."""


def share_function() -> None:
    """Dummy not shared function."""
