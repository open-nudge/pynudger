# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

from pynudger._loader import Class, Function, Path
from pynudger.rule._shared import UtilHelperCommon


class _Common(UtilHelperCommon):
    """Match common and its variations."""

    def regex(self) -> str:
        """Regex matching common(s).

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?common(s)?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "commons" string.

        """
        return "commons"


# Common rules
class CommonClass(_Common, Class, code=12):
    """Rule checking class names for commons."""


class CommonFunction(_Common, Function, code=13):
    """Rule checking function names for commons."""


class CommonPath(_Common, Path, code=14):
    """Rule checking paths for commons."""
