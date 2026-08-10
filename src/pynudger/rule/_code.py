# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared source code line counting."""

from __future__ import annotations

import ast
import typing

from pynudger import _types

if typing.TYPE_CHECKING:
    import collections.abc


def lines(
    root: _types.Node,
    lines: list[str],
    docstring_nodes: collections.abc.Iterable[ast.AST] | None = None,
) -> int:
    """Count executable source lines belonging to an AST node.

    The definition line is included. Decorators are excluded because the
    AST node starts at the definition. Blank lines and comment-only lines are
    excluded before docstring spans are subtracted.

    Args:
        root:
            Module, class, synchronous function, or asynchronous function node
            whose source range is measured.
        lines:
            Source content split into lines.
        docstring_nodes:
            Optional iterable of AST nodes to inspect for docstrings. If it is
            omitted, all descendants of ``root`` are walked. Only module,
            class, and synchronous or asynchronous function nodes contribute
            docstring spans.

    Returns:
        Number of counted source code lines.

    """
    start_line = 1 if isinstance(root, ast.Module) else root.lineno
    end_line = len(lines) if isinstance(root, ast.Module) else root.end_lineno
    selected = (
        lines
        if isinstance(root, ast.Module)
        else lines[start_line - 1 : end_line]
    )

    return (
        len(selected)
        - _non_code(selected)
        - sum(_docstring_sizes(root, lines, docstring_nodes))
    )


def _docstring_sizes(
    root: _types.Node,
    lines: list[str],
    nodes: collections.abc.Iterable[ast.AST] | None = None,
) -> collections.abc.Iterator[int]:
    """Yield source line counts occupied by selected code-node docstrings.

    Args:
        root:
            Module, class, synchronous function, or asynchronous function whose
            subtree is inspected when ``nodes`` is omitted.
        lines:
            Source content split into lines.
        nodes:
            Optional iterable of AST nodes to inspect instead of walking
            ``root``.

    Yields:
        The number of complete source lines occupied by each recognized code
        node's docstring.

    """
    selected = ast.walk(root) if nodes is None else nodes
    types = _types.to_ast(_types.Node)
    for child in selected:
        if (
            isinstance(child, types)
            and ast.get_docstring(child, clean=False) is not None  # pyright: ignore[reportArgumentType]
        ):
            docstring = child.body[0]  # pyright: ignore[reportAttributeAccessIssue]
            docstring_lines = lines[docstring.lineno - 1 : docstring.end_lineno]
            # Deleted lines have to be deleted again here
            # as these are already subtracted in lines
            if docstring.end_lineno is not None:
                yield (len(docstring_lines) - _non_code(docstring_lines))
            else:  # pragma: no cover
                pass


def _non_code(lines: collections.abc.Iterable[str]) -> int:
    """Count non-executable lines in a sequence of source code lines.

    Non-executable lines include blank lines and lines that contain only
    comments (starting with '#').

    Args:
        lines: Sequence of source code lines to analyze.

    Returns:
        Number of non-executable lines.
    """
    non_code = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            non_code += 1
    return non_code
