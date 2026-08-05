# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Analysis for module-local internal definitions."""

from __future__ import annotations

import ast
import dataclasses
import typing

from pynudger.rule import _code

if typing.TYPE_CHECKING:
    import collections.abc

type DefinitionNode = ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
type Definition = tuple[DefinitionNode, str | None]


@dataclasses.dataclass(frozen=True)
class Candidate:
    """Measured module-local definition candidate.

    Attributes:
        node:
            AST node defining the candidate.
        name:
            Definition name.
        owner:
            Owning module-level class name for methods, otherwise ``None``.
        usage_count:
            Number of matching same-file syntactic references.
        code_lines:
            Number of counted source code lines.
    """

    node: DefinitionNode
    name: str
    owner: str | None
    usage_count: int
    code_lines: int


def candidates(
    tree: ast.Module,
    lines: list[str],
    kind: str,
) -> collections.abc.Iterator[Candidate]:
    """Yield every internal candidate of one module-local definition kind.

    Definitions nested in functions or classes are not candidates. Definitions
    in module-level control-flow blocks are candidates. Methods in
    class-level control-flow blocks are candidates when their class is
    module-level.

    Args:
        tree:
            Parsed Python module containing the definitions to analyze.
        lines:
            Source content split into individual lines for code-line counting.
        kind:
            Definition category to yield: ``"function"``, ``"class"``, or
            ``"method"``.

    Yields:
        A ``Candidate`` for each internal definition in the requested
        category.
    """
    for node, owner in _definitions(tree.body):
        if _is_internal(node.name, kind) and _matches_kind(node, owner, kind):
            yield Candidate(
                node=node,
                name=node.name,
                owner=owner,
                usage_count=_usage_count(tree, node, owner),
                code_lines=_code.lines(node, lines),
            )


def _is_internal(name: str, kind: str) -> bool:
    """Return whether a definition name is internal for its category.

    Args:
        name:
            Definition name to classify.
        kind:
            Definition category: ``"function"``, ``"class"``, or
            ``"method"``.

    Returns:
        ``True`` when the name starts with an underscore and, for methods, is
        not a dunder name; otherwise ``False``.
    """
    # Only exclude dunder methods
    return name.startswith("_") and (
        kind != "method" or not name.startswith("__")
    )


def _definitions(
    nodes: collections.abc.Iterable[ast.AST],
    owner: str | None = None,
) -> collections.abc.Iterator[Definition]:
    """Yield module-level definitions and methods in their owning class.

    The traversal enters arbitrary module-level control-flow nodes so that
    definitions inside ``if`` and similar blocks are found. It does not enter
    function bodies or nested classes, because their definitions are not
    candidates for the module-local rules. When traversing a class, its name
    is passed as ``owner`` so that directly contained methods can be identified.

    Args:
        nodes:
            AST nodes to inspect recursively.
        owner:
            Name of the current module-level class, or ``None`` while
            traversing module-level code outside a class.

    Yields:
        ``(definition, owner)`` pairs. The definition is a class or function
        node, and ``owner`` is the owning class name for methods or ``None``
        for module-level definitions.

    """
    for node in nodes:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            yield node, owner
        elif isinstance(node, ast.ClassDef):
            if owner is None:
                yield node, None
                yield from _definitions(node.body, node.name)
            else:  # pragma: no cover
                pass
        else:
            yield from _definitions(ast.iter_child_nodes(node), owner)


def _matches_kind(
    node: DefinitionNode,
    owner: str | None,
    kind: str,
) -> bool:
    """Return whether a definition belongs to the requested category.

    Args:
        node:
            Class or function definition to classify.
        owner:
            Owning class name for a method, or ``None`` for a module-level
            definition.
        kind:
            Requested category: ``"function"``, ``"class"``, or ``"method"``.

    Returns:
        ``True`` when ``node`` has the requested category and ownership level;
        otherwise ``False``.

    """
    is_function = isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    if kind == "class":
        return owner is None and isinstance(node, ast.ClassDef)
    if kind == "method":
        return owner is not None and is_function
    return owner is None and is_function


def _usage_count(
    tree: ast.Module,
    node: DefinitionNode,
    owner: str | None,
) -> int:
    """Count matching same-file references outside a candidate subtree.

    Args:
        tree:
            Parsed module whose AST is searched for references.
        node:
            Function or class definition whose references are counted.
        owner:
            Owning class name for a method, or ``None`` for a module-level
            function or class.

    Returns:
        Number of matching load references outside ``node`` and all of its
        descendants.

    """
    excluded = {id(child) for child in ast.walk(node)}
    return sum(
        1
        for reference in ast.walk(tree)
        if id(reference) not in excluded
        and _is_usage(reference, node.name, owner)
    )


def _is_usage(
    reference: ast.AST,
    name: str,
    owner: str | None,
) -> bool:
    """Return whether an AST node is a matching load reference.

    Args:
        reference:
            AST node to inspect.
        name:
            Definition name being searched for.
        owner:
            Owning class name for a method, or ``None`` for a module-level
            definition.

    Returns:
        ``True`` for a matching loaded name or direct method attribute
        reference; otherwise ``False``.

    """
    if owner is None:
        return (
            isinstance(reference, ast.Name)
            and reference.id == name
            and isinstance(reference.ctx, ast.Load)
        )
    return (
        isinstance(reference, ast.Attribute)
        and reference.attr == name
        and isinstance(reference.ctx, ast.Load)
        and isinstance(reference.value, ast.Name)
        and reference.value.id in ("self", "cls", owner)
    )
