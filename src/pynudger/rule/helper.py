# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

from pynudger._loader import Class, Function, Path
from pynudger.rule._shared import UtilHelperCommon


class _Helper(UtilHelperCommon):
    """Match helpers and its variations."""

    def regex(self) -> str:
        """Regex matching helpers.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?help(ers?)?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "helpers" string.

        """
        return "helpers"


# Helper rules
class HelperClass(_Helper, Class, code=9):
    """Rule checking class names for helpers."""


class HelperFunction(_Helper, Function, code=10):
    """Rule checking function names for helpers."""


class HelperPath(_Helper, Path, code=11):
    """Rule checking paths for helpers."""
