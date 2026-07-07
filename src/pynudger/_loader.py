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
    from collections.abc import Iterable

# Shared functionality


class _Definition(lintkit.loader.Python, lintkit.rule.Node, abc.ABC):
    """Base class for loading configured AST nodes."""

    @abc.abstractmethod
    def ast_classes(self) -> tuple[type[ast.AST]]:
        """Return the AST class to look for.

        Returns:
            AST class to look for

        """
        raise NotImplementedError

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield all values of the specified AST class.

        Yields:
            All values of the specified AST class.

        """
        data: dict[type[ast.AST], list[ast.AST]] = self.getitem("nodes_map")
        for ast_class in self.ast_classes():
            for node in data[ast_class]:
                yield lintkit.Value.from_python(
                    self._unpack(node),
                    node,
                )

    def _unpack(self, node: ast.AST) -> str:
        """Extract the value from a node.

        Args:
            node:
                The AST node to extract the value from.

        Returns:
            The value loaded from the node.

        """
        return node.name  # pyright: ignore[reportAttributeAccessIssue]


# Concrete loaders


class Class(_Definition, abc.ABC):
    """Loader for class definitions."""

    def ast_classes(self) -> tuple[type[ast.AST], ...]:
        """Return the AST classes to look for.

        Returns:
            Always ast.ClassDef

        """
        return (ast.ClassDef,)


class Function(_Definition, abc.ABC):
    """Loader for function definitions."""

    def ast_classes(self) -> tuple[type[ast.AST], ...]:
        """Return the AST classes to look for.

        Returns:
            Always ast.FunctionDef

        """
        return (ast.FunctionDef,)


class Return(_Definition, abc.ABC):
    """Loader for return statements."""

    def ast_classes(self) -> tuple[type[ast.AST], ...]:
        """Return the AST classes to look for.

        Returns:
            Always ast.Return

        """
        return (ast.Return,)

    def _unpack(self, node: ast.Return) -> ast.expr | None:
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

    def ast_classes(self) -> tuple[type[ast.AST], ...]:
        """Return the AST classes to look for.

        Returns:
            Always ast.Attribute

        """
        return (ast.Attribute,)

    def _unpack(self, node: ast.Attribute) -> str:
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

    def ast_classes(self) -> tuple[type[ast.AST], ...]:
        """Return the AST classes to look for.

        Returns:
            Always ast.Call

        """
        return (ast.Call,)

    def _unpack(self, node: ast.Call) -> str:
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

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield the file path as a value.

        Yields:
            The file path as a value
        """
        # COE: lintkit framework assures self.file is not None at this point
        yield lintkit.Value(str(self.file.stem))  # pyright: ignore[reportOptionalMemberAccess]


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
