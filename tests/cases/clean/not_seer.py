# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Testing setters rule violations."""
# noqa-file: PYNUDGER43, PYNUDGER46

from __future__ import annotations


class NotSer:
    """Dummy not setter class."""


def not_ser() -> None:
    """Dummy not setter function."""
