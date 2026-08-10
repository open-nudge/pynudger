# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared Python AST types."""

from __future__ import annotations

import ast
import functools
import typing

type AssignmentNode = ast.Assign | ast.AnnAssign | ast.AugAssign
type FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef
type DefinitionNode = ast.ClassDef | FunctionNode
type GlobalDefinitionNode = ast.Name | DefinitionNode
type Node = ast.Module | DefinitionNode
type YieldNode = ast.Yield | ast.YieldFrom
type NodeMap = dict[type[ast.AST], list[ast.AST]]
type Definition = tuple[DefinitionNode, str | None]


@functools.cache
def to_ast(
    alias: typing.TypeAliasType,
) -> tuple[type[ast.AST], ...]:
    """Return concrete AST classes from a nested type alias.

    Args:
        alias:
            Acyclic internal type alias to expand.

    Returns:
        Concrete AST classes represented by the alias.

    """
    return tuple(
        node_type
        for member in typing.get_args(alias.__value__)
        for node_type in (
            to_ast(member)
            if isinstance(member, typing.TypeAliasType)
            else (member,)
        )
    )
