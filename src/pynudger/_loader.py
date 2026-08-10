# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger loaders."""

from __future__ import annotations

import abc
import ast
import itertools
import typing

import lintkit

from pynudger import _node

if typing.TYPE_CHECKING:
    import collections.abc

    from pynudger import _types

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
    ) -> collections.abc.Iterable[_types.FunctionNode]:
        """Yield function definition nodes in their existing loader order.

        Returns:
            Synchronous definitions followed by asynchronous definitions.

        """
        return itertools.chain.from_iterable(
            self.getitem("nodes_map")[t]
            for t in [ast.FunctionDef, ast.AsyncFunctionDef]
        )


class GlobalDefinition(_Definition, abc.ABC):
    """Loader for supported module-scope declarations."""

    def nodes(
        self,
    ) -> collections.abc.Iterable[_types.GlobalDefinitionNode]:
        """Return declarations from module-level control flow.

        Returns:
            Iterable of declarations outside class and function bodies.

        """
        tree: ast.Module = self.getitem("ast")
        return _node.global_nodes(tree)


class Type(_Definition, abc.ABC):
    """Loader for explicit type-expression roots."""

    def nodes(self) -> collections.abc.Iterable[ast.expr]:
        """Yield explicit type-expression roots in grouped AST order.

        Yields:
            Annotation, return, alias, and type-variable bound expressions.

        """
        maybe_annotated = itertools.chain.from_iterable(
            self.getitem("nodes_map")[t] for t in [ast.AnnAssign, ast.arg]
        )
        maybe_returns = itertools.chain.from_iterable(
            self.getitem("nodes_map")[t]
            for t in [ast.FunctionDef, ast.AsyncFunctionDef]
        )
        maybe_bound = self.getitem("nodes_map")[ast.TypeVar]
        maybe_value = self.getitem("nodes_map")[ast.TypeAlias]

        for field, nodes in zip(
            ("annotation", "returns", "bound", "value"),
            (maybe_annotated, maybe_returns, maybe_bound, maybe_value),
            strict=True,
        ):
            for node in nodes:
                if (value := getattr(node, field)) is not None:
                    yield value


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
        return _node.call_name(node.func)


class Path(lintkit.loader.File, lintkit.rule.Node, abc.ABC):
    """Loader for file paths."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[str]]:
        """Yield the file path as a value.

        Yields:
            The file path as a value
        """
        # enq: lintkit framework assures self.file is not None at this point
        yield lintkit.Value(str(self.file.stem))  # pyright: ignore[reportOptionalMemberAccess]
