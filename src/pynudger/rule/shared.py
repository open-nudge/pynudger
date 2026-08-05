# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

from pynudger._loader import Class, Function, Path
from pynudger.rule._shared import UtilHelperCommon


class _Shared(UtilHelperCommon):
    """Match shared and its variations."""

    def regex(self) -> str:
        """Regex matching shared.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?shared"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "shared" string.

        """
        return "shared"


# Shared rules
class SharedClass(_Shared, Class, code=15):
    """Rule checking class names for shared."""


class SharedFunction(_Shared, Function, code=16):
    """Rule checking function names for shared."""


class SharedPath(_Shared, Path, code=17):
    """Rule checking paths for shared."""
