# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rule limiting nested type subscripts."""

from __future__ import annotations

import ast
import typing

import lintkit

from pynudger._loader import Type

if typing.TYPE_CHECKING:
    import collections.abc


class Depth(lintkit.check.Check, Type, code=45):
    """Rule checking type expressions with deeply nested subscripts."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[int]]:
        """Yield the subscript depth of every explicit type root.

        Yields:
            Maximum nested subscript depth for each explicit type root.

        """
        for root in super().nodes():
            yield lintkit.Value.from_python(_depth(root), root)

    def check(self, value: lintkit.Value[int]) -> bool:
        """Report subscript depths above the configured maximum.

        Args:
            value:
                Maximum nested subscript depth in the type root.

        Returns:
            True when the type depth exceeds the configured maximum.

        """
        return value > self._max_depth()

    def message(self, value: lintkit.Value[int]) -> str:
        """Describe a type root that exceeds the depth limit.

        Args:
            value:
                Maximum nested subscript depth in the type root.

        Returns:
            Diagnostic containing the actual and maximum type depths.

        """
        return (
            f"Type has depth {value}, which exceeds the maximum of "
            f"{self._max_depth()}."
        )

    def description(self) -> str:
        """Return the public rule description.

        Returns:
            Description of the nested type depth limit.

        """
        return "Avoid deeply nested types."

    def _max_depth(self) -> int:
        """Return the configured maximum type depth.

        Returns:
            Maximum allowed nested subscript depth.

        """
        return self.config.get("max_type_depth", 1)  # pyright: ignore[reportAttributeAccessIssue]


def _depth(node: ast.AST) -> int:
    """Return the maximum nested subscript depth below a syntax node.

    Args:
        node:
            Syntax node to inspect.

    Returns:
        Maximum number of nested subscript nodes.

    """
    children = (_depth(child) for child in ast.iter_child_nodes(node))
    return max(children, default=0) + isinstance(node, ast.Subscript)
