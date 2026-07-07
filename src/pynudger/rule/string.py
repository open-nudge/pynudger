# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Registered string rules."""

from __future__ import annotations

import ast

import lintkit

from pynudger._loader import Return


class EmptyReturn(
    lintkit.check.Check,
    Return,
    code=27,
):
    """Rule checking empty string return values."""

    def check(self, value: lintkit.Value[ast.expr | None]) -> bool:
        """Report every loaded value as a rule violation.

        Args:
            value:
                Return value to check

        Returns:
            True if the value is constant and an empty string,
            False otherwise.

        """
        return isinstance(value, ast.Constant) and value.value == ""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid returning empty strings. Return None to indicate lack of value."

    def message(self, _: lintkit.Value[str]) -> str:
        """Return an empty string return violation message.

        Args:
            _:
                Empty string return value.

        Returns:
            Message describing the rule violation.

        """
        return self.description()
