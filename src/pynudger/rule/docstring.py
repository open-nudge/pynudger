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

from pynudger._loader import Function

if typing.TYPE_CHECKING:
    import collections.abc

type FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef
type FunctionOwners = set[FunctionNode]


class Arguments(
    lintkit.check.Check,
    Function,
    code=34,
):
    """Rule checking missing Args docstring sections."""

    def check(
        self,
        function: lintkit.Value[FunctionNode],
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
        _: lintkit.Value[ast.FunctionDef | ast.AsyncFunctionDef],
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
    lintkit.loader.Python,
    lintkit.rule.Node,
    abc.ABC,
):
    """Base rule matching docstring sections owned by functions."""

    @abc.abstractmethod
    def _predicate(
        self, function: FunctionNode, owners: FunctionOwners
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
        nodes_map: dict[type[ast.AST], list[ast.AST]] = self.getitem(
            "nodes_map"
        )
        functions: list[FunctionNode] = [
            function
            for function in nodes_map[ast.FunctionDef]
            + nodes_map[ast.AsyncFunctionDef]
            if isinstance(function, ast.FunctionDef | ast.AsyncFunctionDef)
        ]
        yield_nodes: list[ast.Yield | ast.YieldFrom] = [
            yield_node
            for yield_node in nodes_map[ast.Yield] + nodes_map[ast.YieldFrom]
            if isinstance(yield_node, ast.Yield | ast.YieldFrom)
        ]
        owners: FunctionOwners = {
            self._owner(yield_node, functions) for yield_node in yield_nodes
        }

        for function in functions:
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

    def _owner(
        self,
        yield_node: ast.Yield | ast.YieldFrom,
        functions: list[FunctionNode],
    ) -> FunctionNode:
        """Return the innermost function owning a yield expression.

        This is necessary to infer whether our current function is
        a generator expression or not.

        Args:
            yield_node:
                Yield expression to locate within the parsed functions.
            functions:
                Function definitions that may contain the yield expression.

        Returns:
            Innermost function definition containing the yield expression.

        """
        yield_end_lineno = yield_node.end_lineno
        yield_end_col_offset = yield_node.end_col_offset

        containing = [
            function
            for function in functions
            if function.end_lineno is not None
            and function.end_col_offset is not None
            if (
                (function.lineno, function.col_offset)
                <= (yield_node.lineno, yield_node.col_offset)
                and (yield_end_lineno, yield_end_col_offset)
                <= (
                    function.end_lineno,
                    function.end_col_offset,
                )
            )
        ]
        return min(
            containing,
            key=lambda function: (  # pyright: ignore[reportUnknownLambdaType]
                function.end_lineno - function.lineno,  # pyright: ignore[reportOptionalOperand]
                function.end_col_offset - function.col_offset,  # pyright: ignore[reportOptionalOperand]
            ),
        )


class Yields(_Owner, code=35):
    """Rule checking missing Yields docstring sections."""

    def _predicate(
        self, function: FunctionNode, owners: FunctionOwners
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
        self, function: FunctionNode, owners: FunctionOwners
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
