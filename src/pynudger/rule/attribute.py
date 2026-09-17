# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Registered restricted construct rules."""

from __future__ import annotations

import ast
import typing

import lintkit

from pynudger._loader import Attribute

if typing.TYPE_CHECKING:
    import collections.abc


class Dunder(lintkit.check.Check, Attribute, code=29):
    """Rule checking restricted explicit dunder attribute access."""

    def nodes(self) -> collections.abc.Iterable[ast.Attribute]:
        """Yield attributes without a direct `super` receiver.

        Yields:
            Attribute nodes without a direct `super` receiver.
        """
        for node in super().nodes():
            receiver = node.value
            if (
                isinstance(receiver, ast.Call)
                and isinstance(receiver.func, ast.Name)
                and receiver.func.id == "super"
            ):
                continue
            yield node

    def check(self, value: lintkit.Value[typing.Any]) -> bool:
        """Check if the attribute name starts with double underscores.

        Args:
            value:
                Loaded attribute construct.

        Returns:
            ``True`` if the attribute name starts with double underscores.
        """
        return value.startswith("__")

    def description(self) -> str:
        """Return rule description.

        Returns:
            Rule description string.
        """
        return (
            "Avoid explicit dunder usage (attributes starting with __) "
            "except directly through super(...)."
        )

    def message(self, value: lintkit.Value[str]) -> str:
        """Return a restricted construct violation message.

        Args:
            value:
                Restricted construct name.

        Returns:
            Message describing the restricted construct.

        """
        return f"Avoid explicit dunder usage: '{value}'"
