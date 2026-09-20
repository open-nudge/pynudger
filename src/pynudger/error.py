# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Report invalid inputs to pynudger rules."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import ast


class PynudgerError(Exception):
    """Base exception for pynudger rule errors."""


class UnsupportedNodeError(PynudgerError):
    """Report an AST node with no declaration kind."""

    def __init__(self, node: ast.AST) -> None:  # pragma: no cover
        """Name the unsupported node type.

        Args:
            node: AST node that cannot be classified.
        """
        super().__init__(f"Unsupported node type: {type(node).__name__}")


class InvalidStrategyError(PynudgerError):
    """Report an unknown assignment strategy."""

    def __init__(self, strategy: str) -> None:  # pragma: no cover
        """Name the invalid strategy value.

        Args:
            strategy: Strategy value supplied by the caller.
        """
        super().__init__(f"Invalid assignment strategy: {strategy}")
