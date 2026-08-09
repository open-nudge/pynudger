# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Testing no accidental 'common' rule violations."""
# noqa-file: PYNUDGER43

from __future__ import annotations


class ComonClass:
    """Dummy not common class."""


def comon_function() -> None:
    """Dummy not common function."""
