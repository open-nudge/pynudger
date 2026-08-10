# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rule limiting pipe type union members."""

from __future__ import annotations

import ast
import typing

import lintkit

from pynudger._loader import Type

if typing.TYPE_CHECKING:
    import collections.abc


class Union(lintkit.check.Check, Type, code=44):
    """Rule checking pipe type unions with too many members."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[int]]:
        """Yield direct-member counts for every pipe type union.

        Yields:
            Direct-member count for each pipe type union in every type root.

        """
        for root in super().nodes():
            for node in _unions(root):
                count = sum(1 for _ in _pipe_members(node))
                yield lintkit.Value.from_python(count, node)

    def check(self, value: lintkit.Value[int]) -> bool:
        """Report union member counts above the configured maximum.

        Args:
            value:
                Number of syntactic members in a pipe type union.

        Returns:
            True when the union exceeds the configured maximum.

        """
        return value > self._max_types()

    def message(self, value: lintkit.Value[int]) -> str:
        """Describe a pipe type union that exceeds the limit.

        Args:
            value:
                Number of syntactic members in the pipe type union.

        Returns:
            Diagnostic containing the actual and maximum member counts.

        """
        return (
            f"Type union has {value} members, which exceeds the maximum of "
            f"{self._max_types()}."
        )

    def description(self) -> str:
        """Return the public rule description.

        Returns:
            Description of the pipe type union member limit.

        """
        return "Avoid pipe type unions with too many members."

    def _max_types(self) -> int:
        """Return the configured maximum number of union members.

        Returns:
            Maximum allowed member count.

        """
        return self.config.get("max_union_types", 3)  # pyright: ignore[reportAttributeAccessIssue]


def _unions(
    node: ast.AST,
) -> collections.abc.Iterator[ast.BinOp]:
    """Yield pipe unions and inspect their direct members separately.

    Args:
        node:
            Type expression to inspect.

    Yields:
        Each connected pipe expression once.

    """
    if _is_pipe(node):
        yield node
        for member in _pipe_members(node):
            yield from _unions(member)
        return
    for child in ast.iter_child_nodes(node):
        yield from _unions(child)


def _pipe_members(node: ast.BinOp) -> collections.abc.Iterator[ast.expr]:
    """Yield operands from one connected pipe expression.

    Args:
        node:
            Pipe expression to flatten.

    Yields:
        Direct operands after flattening connected pipe expressions.

    """
    for member in (node.left, node.right):
        if _is_pipe(member):
            yield from _pipe_members(member)
        else:
            yield member


def _is_pipe(node: ast.AST) -> typing.TypeGuard[ast.BinOp]:
    """Return whether a node is a pipe union expression.

    Args:
        node:
            Syntax node to classify.

    Returns:
        True for a binary operation with the pipe operator.

    """
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr)
