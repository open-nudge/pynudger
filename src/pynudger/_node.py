# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared Python AST node analysis."""

from __future__ import annotations

import ast
import typing

from pynudger import _types

if typing.TYPE_CHECKING:
    import collections.abc


def global_nodes(
    node: ast.AST,
) -> collections.abc.Iterable[_types.GlobalDefinitionNode]:
    """Yield supported declarations without entering definition scopes.

    Args:
        node:
            Current node in the module-scope traversal.

    Yields:
        Assignment names, classes, and functions.

    """
    if isinstance(node, _types.to_ast(_types.DefinitionNode)):
        yield node  # pyright: ignore[reportReturnType]
        return
    if isinstance(node, _types.to_ast(_types.AssignmentNode)):
        targets: collections.abc.Iterable[ast.expr] = (
            node.targets if isinstance(node, ast.Assign) else (node.target,)  # pyright: ignore[reportAttributeAccessIssue]
        )
        yield from (
            name
            for target in targets
            for name in ast.walk(target)  # pyright: ignore[reportUnknownArgumentType]
            if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store)
        )
        return
    for child in ast.iter_child_nodes(node):
        yield from global_nodes(child)


def call_name(node: ast.AST) -> str:
    """Extract the fully qualified name of a call target.

    Args:
        node:
            Call target node to unwrap.

    Returns:
        Name identifier or empty string.

    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{call_name(node.value)}.{node.attr}"
    return ""  # pragma: no cover
