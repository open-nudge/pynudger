# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger loaders."""

from __future__ import annotations

import abc
import ast
import typing

import lintkit

if typing.TYPE_CHECKING:
    import collections.abc

type GlobalDefinitionNode = (
    ast.Name | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
)

# Shared functionality


class _Definition(lintkit.loader.Python, lintkit.rule.Node, abc.ABC):
    """Base class for loading configured AST nodes."""

    @abc.abstractmethod
    def nodes(self) -> collections.abc.Iterable[ast.AST]:
        """Return the configured AST nodes.

        Returns:
            Iterable of AST nodes handled by the concrete loader.

        """
        raise NotImplementedError

    def values(
        self,
    ) -> collections.abc.Iterable[lintkit.Value[typing.Any]]:
        """Wrap values from the configured AST nodes.

        Yields:
            Values extracted from the configured AST nodes.

        """
        for node in self.nodes():
            yield lintkit.Value.from_python(self.unpack(node), node)

    def unpack(self, node: ast.AST) -> typing.Any:
        """Extract the value from a node.

        Args:
            node:
                The AST node to extract the value from.

        Returns:
            The value loaded from the node.

        """
        return node.name  # pyright: ignore[reportAttributeAccessIssue]


# Concrete loaders


class Variable(_Definition, abc.ABC):
    """Loader for variable binding names."""

    def nodes(self) -> collections.abc.Iterable[ast.Name]:
        """Yield names bound by store operations in all scopes.

        Yields:
            ``ast.Name`` nodes with ``ast.Store`` context.

        """
        data: list[ast.Name] = self.getitem("nodes_map")[ast.Name]
        for node in data:
            if isinstance(node.ctx, ast.Store):
                yield node

    def unpack(self, node: ast.Name) -> str:
        """Extract the value from a node.

        Args:
            node:
                The AST node to extract the value from.

        Returns:
            The value loaded from the node.

        """
        return node.id


class Class(_Definition, abc.ABC):
    """Loader for class definitions."""

    def nodes(self) -> collections.abc.Iterable[ast.ClassDef]:
        """Return class definition nodes in their existing loader order.

        Returns:
            Iterable of ``ast.ClassDef`` nodes.

        """
        return self.getitem("nodes_map")[ast.ClassDef]


class Function(_Definition, abc.ABC):
    """Loader for function definitions."""

    def nodes(
        self,
    ) -> collections.abc.Iterable[ast.FunctionDef | ast.AsyncFunctionDef]:
        """Yield function definition nodes in their existing loader order.

        Yields:
            Synchronous definitions followed by asynchronous definitions.

        """
        functions: list[ast.FunctionDef] = self.getitem("nodes_map")[
            ast.FunctionDef
        ]
        async_functions: list[ast.AsyncFunctionDef] = self.getitem("nodes_map")[
            ast.AsyncFunctionDef
        ]
        yield from functions
        yield from async_functions


class GlobalDefinition(_Definition, abc.ABC):
    """Loader for supported module-scope declarations."""

    def nodes(
        self,
    ) -> collections.abc.Iterable[GlobalDefinitionNode]:
        """Return declarations from module-level control flow.

        Returns:
            Iterable of declarations outside class and function bodies.

        """
        tree: ast.Module = self.getitem("ast")
        return _global_nodes(tree)


class Return(_Definition, abc.ABC):
    """Loader for return statements."""

    def nodes(self) -> collections.abc.Iterable[ast.Return]:
        """Return statement nodes.

        Returns:
            Iterable of ``ast.Return`` nodes.

        """
        return self.getitem("nodes_map")[ast.Return]

    def unpack(self, node: ast.Return) -> ast.expr | None:
        """Unwrap a return node to extract the returned value.

        Args:
            node:
                The return node to unwrap.

        Returns:
            Returned value node.

        """
        return node.value


class Attribute(_Definition, abc.ABC):
    """Loader for attribute access nodes."""

    def nodes(self) -> collections.abc.Iterable[ast.Attribute]:
        """Return attribute access nodes.

        Returns:
            Iterable of ``ast.Attribute`` nodes.

        """
        return self.getitem("nodes_map")[ast.Attribute]

    def unpack(self, node: ast.Attribute) -> str:
        """Unwrap an attribute node to extract the attribute name.

        Args:
            node:
                The attribute node to unwrap.

        Returns:
            Attribute name.

        """
        return node.attr


class Call(_Definition, abc.ABC):
    """Load restricted runtime calls by direct syntactic name."""

    def nodes(self) -> collections.abc.Iterable[ast.Call]:
        """Return function call nodes.

        Returns:
            Iterable of ``ast.Call`` nodes.

        """
        return self.getitem("nodes_map")[ast.Call]

    def unpack(self, node: ast.Call) -> str:
        """Unwrap a function call node to extract the fully qualified name.

        Args:
            node:
                The function call node to unwrap.

        Returns:
            Name identifier or empty string.

        """
        return _call_unpack(node.func)


class Path(lintkit.loader.File, lintkit.rule.Node, abc.ABC):
    """Loader for file paths."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[str]]:
        """Yield the file path as a value.

        Yields:
            The file path as a value
        """
        # enq: lintkit framework assures self.file is not None at this point
        yield lintkit.Value(str(self.file.stem))  # pyright: ignore[reportOptionalMemberAccess]


def _global_nodes(
    node: ast.AST,
) -> collections.abc.Iterable[GlobalDefinitionNode]:
    """Yield supported declarations without entering definition scopes.

    Args:
        node:
            Current node in the module-scope traversal.

    Yields:
        Assignment names, classes, and functions.

    """
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        yield node
        return
    if isinstance(node, ast.Assign | ast.AnnAssign | ast.AugAssign):
        targets = (
            node.targets if isinstance(node, ast.Assign) else (node.target,)
        )
        yield from (
            name
            for target in targets
            for name in ast.walk(target)
            if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store)
        )
        return
    for child in ast.iter_child_nodes(node):
        yield from _global_nodes(child)


def _call_unpack(node: ast.AST) -> str:
    """Unwrap a function call node to extract the fully qualified name.

    Args:
        node:
            The function call node to unwrap.

    Returns:
        Name identifier or empty string.

    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_call_unpack(node.value)}.{node.attr}"

    # Graceful return that should never happen under normal circumstances
    return ""  # pragma: no cover
