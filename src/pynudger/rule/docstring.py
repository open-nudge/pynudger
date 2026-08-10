# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules validating docstring sections."""

from __future__ import annotations

import abc
import ast
import typing

import lintkit

from pynudger import _types
from pynudger._loader import Function

if typing.TYPE_CHECKING:
    import collections.abc

type FunctionOwners = set[_types.FunctionNode]


class Arguments(
    lintkit.check.Check,
    Function,
    code=34,
):
    """Rule checking missing Args docstring sections."""

    def check(
        self,
        function: lintkit.Value[_types.FunctionNode],
    ) -> bool:
        """Report functions missing an Args section.

        Args:
            function:
                Function definition checking for an Args section.

        Returns:
            `True` if necessary `Args:` section is missing in docstring.

        """
        arguments = function.args
        names = [
            argument.arg
            for argument in (
                arguments.posonlyargs + arguments.args + arguments.kwonlyargs
            )
        ]
        if arguments.vararg is not None:
            names.append(arguments.vararg.arg)  # pyright: ignore[reportUnknownArgumentType]
        if arguments.kwarg is not None:
            names.append(arguments.kwarg.arg)  # pyright: ignore[reportUnknownArgumentType]

        real_arguments = [name for name in names if name not in ("self", "cls")]
        return real_arguments and (  # pyright: ignore[reportReturnType]
            "Args:" not in (ast.get_docstring(function, clean=False) or "")
        )

    def description(self) -> str:
        """Return rule description.

        Returns:
            Human-readable rule description.

        """
        return "Avoid undocumented function parameters. Add an Args: section."

    def message(
        self,
        _: lintkit.Value[_types.FunctionNode],
    ) -> str:
        """Return missing Args section violation message.

        Args:
            _:
                Function definition requiring an Args section.

        Returns:
            Message describing the missing Args section.

        """
        return self.description()

    def unpack(self, node: ast.AST) -> ast.AST:
        """Extract the value from a node.

        Args:
            node:
                The AST node to extract the value from.

        Returns:
            The value loaded from the node.

        """
        return node


class _Owner(
    lintkit.check.Check,
    Function,
    abc.ABC,
):
    """Base rule matching docstring sections owned by functions."""

    @abc.abstractmethod
    def _predicate(
        self,
        function: _types.FunctionNode,
        owners: FunctionOwners,
    ) -> bool:
        """Return whether a function is a section violation.

        Args:
            function:
                Function definition checking for a section.
            owners:
                Functions owning matching yield expressions.

        Returns:
            True if the function should be reported.

        """
        raise NotImplementedError

    def values(
        self,
    ) -> collections.abc.Iterable[lintkit.Value[None]]:
        """Yield functions missing their required docstring section.

        Yields:
            Function definitions requiring a docstring section.

        """
        tree: ast.Module = self.getitem("ast")
        owners: FunctionOwners = set(_owners(tree))

        for function in self.nodes():
            if self._predicate(function, owners):
                # Dummy value as check is always True
                yield lintkit.Value.from_python(None, function)

    def check(
        self,
        _: lintkit.Value[None],
    ) -> bool:
        """Report every prefiltered function as a rule violation.

        Args:
            _:
                Function definition requiring a docstring section.

        Returns:
            Always True as values are prefiltered violations.

        """
        return True


class Yields(_Owner, code=35):
    """Rule checking missing Yields docstring sections."""

    def _predicate(
        self,
        function: _types.FunctionNode,
        owners: FunctionOwners,
    ) -> bool:
        """Return whether a function misses a Yields section.

        Args:
            function:
                Function definition checking for a Yields section.
            owners:
                Functions owning yield expressions.

        Returns:
            True if the function is a generator missing a Yields section.

        """
        docstring = ast.get_docstring(function, clean=False) or ""
        return function in owners and "Yields:" not in docstring

    def description(self) -> str:
        """Return rule description.

        Returns:
            Human-readable rule description.

        """
        return "Avoid undocumented generator yields. Add a Yields: section."

    def message(
        self,
        _: lintkit.Value[None],
    ) -> str:
        """Return missing Yields section violation message.

        Args:
            _:
                Function definition requiring a Yields section.

        Returns:
            Message describing the missing Yields section.

        """
        return self.description()


class Returns(_Owner, code=36):
    """Rule checking missing Returns docstring sections."""

    def _predicate(
        self,
        function: _types.FunctionNode,
        owners: FunctionOwners,
    ) -> bool:
        """Return whether a function misses a Returns section.

        Args:
            function:
                Function definition checking for a Returns section.
            owners:
                Functions owning yield expressions.

        Returns:
            True if the function has a return annotation requiring docs.

        """
        return (
            function not in owners
            and function.returns is not None
            and not (
                isinstance(function.returns, ast.Constant)
                and function.returns.value is None
            )
            and "Returns:"
            not in (ast.get_docstring(function, clean=False) or "")
        )

    def description(self) -> str:
        """Return rule description.

        Returns:
            Human-readable rule description.

        """
        return "Avoid undocumented return values. Add a Returns: section."

    def message(
        self,
        _: lintkit.Value[None],
    ) -> str:
        """Return missing Returns section violation message.

        Args:
            _:
                Function definition requiring a Returns section.

        Returns:
            Message describing the missing Returns section.

        """
        return self.description()


def _owners(
    node: ast.AST,
    owner: _types.FunctionNode | None = None,
) -> collections.abc.Iterable[_types.FunctionNode]:
    """Yield the innermost function owning each yield expression.

    Args:
        node:
            AST node whose children to traverse.
        owner:
            Innermost function containing the current node.

    Yields:
        Function owning each yield or yield-from expression.

    """
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
        owner = node
    if isinstance(node, ast.Yield | ast.YieldFrom) and owner is not None:
        yield owner

    for child in ast.iter_child_nodes(node):
        yield from _owners(child, owner)
