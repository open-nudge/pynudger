# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test no accidental attribute rules violations."""

from __future__ import annotations


class NotDunder:
    """Dunder class."""

    def _dict__(self) -> int:
        """Return a private attribute."""
        return 42

    def not_dunder(self) -> int:
        """Return properties.

        Should **NOT** violate attribute rule 26 (dunder method).

        Returns:
            Almost private __dict__ attribute.

        """
        return self._dict__()
