# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test no accidental attribute rules violations."""

# noqa-file: PYNUDGER46

from __future__ import annotations


class NotDunder:
    """Dunder class."""

    def __init__(self) -> None:
        """Initialize through both forms of direct `super` access."""
        super().__init__()
        super(NotDunder, self).__init__()  # noqa: UP008

    def _dict__(self) -> int:
        """Return a private attribute.

        Returns:
            Private attribute value.

        """
        return 42

    def not_dunder(self) -> int:
        """Return properties.

        Should **NOT** violate attribute rule 26 (dunder method).

        Returns:
            Almost private __dict__ attribute.

        """
        return self._dict__() + self._dict__()

    def parent_string(self) -> str:
        """Return the parent's string representation.

        Returns:
            Parent string representation.
        """
        return super().__str__()
