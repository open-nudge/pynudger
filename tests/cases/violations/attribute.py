# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test attribute rules violations."""

from __future__ import annotations

import typing


class Dunder:
    """Dunder class."""

    @property
    def dunder(self) -> dict[str, typing.Any]:
        """Return properties.

        Should violate attribute rule 26 (dunder method).

        Returns:
            Dictionary containing instance attributes.

        """
        return self.__dict__
