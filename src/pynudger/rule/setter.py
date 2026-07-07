# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

from pynudger._loader import Class, Function, Path
from pynudger.rule._shared import SetGet


class _Set(SetGet):
    """Match setter and its variations."""

    def regex(self) -> str:
        """Regex matching setters.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"^_?set(?:s|ters?)?_?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "setters" string.

        """
        return "setters"


# Setter rules
class SetClass(_Set, Class, code=0):
    """Rule checking class names for setters."""


class SetFunction(_Set, Function, code=1):
    """Rule checking function names for setters."""


class SetPath(_Set, Path, code=2):
    """Rule checking paths for setters."""
