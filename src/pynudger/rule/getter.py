# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

from pynudger._loader import Class, Function, Path
from pynudger.rule._shared import SetGet


class _Get(SetGet):
    """Match getter and its variations."""

    def regex(self) -> str:
        """Regex matching getters.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"^_?get(?:s|ters?)?_?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "getters" string.

        """
        return "getters"


# Getters rules
class GetClass(_Get, Class, code=3):
    """Rule checking class names for getters."""


class GetFunction(_Get, Function, code=4):
    """Rule checking function names for getters."""


class GetPath(_Get, Path, code=5):
    """Rule checking paths for getters."""
