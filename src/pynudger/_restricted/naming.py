# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""AST name extraction helpers."""

from __future__ import annotations

import ast


def plain(node: ast.expr) -> str | None:
    """Return a plain name expression.

    Args:
        node:
            Expression to check.

    Returns:
        Name identifier or ``None``.

    """
    if isinstance(node, ast.Name):
        return node.id
    return None


def call(node: ast.expr) -> str | None:
    """Return a direct runtime call name.

    Args:
        node:
            Call function expression.

    Returns:
        Direct call name, exact ``typing.cast`` call, or ``None``.

    """
    if _is_typing_cast(node):
        return "typing.cast"
    return plain(node)


def decorator(node: ast.expr) -> str | None:
    """Return a direct decorator name.

    Args:
        node:
            Decorator expression.

    Returns:
        Direct decorator name or ``None``.

    """
    if isinstance(node, ast.Call):
        return call(node.func)
    return plain(node)


def _is_typing_cast(node: ast.expr) -> bool:
    """Check whether an expression is exactly ``typing.cast``.

    Args:
        node:
            Expression to check.

    Returns:
        ``True`` when expression is exactly ``typing.cast``.

    """
    if not isinstance(node, ast.Attribute):
        return False
    if not isinstance(node.value, ast.Name):
        return False
    return node.value.id == "typing" and node.attr == "cast"
