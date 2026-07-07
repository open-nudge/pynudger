# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

from pynudger._loader import Class, Function, Path
from pynudger.rule._shared import UtilHelperCommon


class _Util(UtilHelperCommon):
    """Match utilities and its variations."""

    def regex(self) -> str:
        """Regex matching utils.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?util(s|ities)?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "utils" string.

        """
        return "utils"


# Util rules
class UtilClass(_Util, Class, code=6):
    """Rule checking class names for utils."""


class UtilFunction(_Util, Function, code=7):
    """Rule checking function names for utils."""


class UtilPath(_Util, Path, code=8):
    """Rule checking paths for utils."""
