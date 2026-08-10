# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules validating keyword usage."""

from __future__ import annotations

import abc
import ast
import typing

import lintkit

from pynudger._loader import _Definition

if typing.TYPE_CHECKING:
    import collections.abc

    from pynudger import _types


class _Keyword(lintkit.check.Check, _Definition, abc.ABC):
    """Rule checking restricted state management keywords."""

    def nodes(self) -> collections.abc.Iterable[ast.AST]:
        """Yield restricted keyword nodes in configured class order.

        Yields:
            AST nodes for each restricted keyword class.

        """
        data: _types.NodeMap = self.getitem("nodes_map")
        for ast_class in self.ast_classes():
            yield from data[ast_class]

    @abc.abstractmethod
    def ast_classes(self) -> tuple[type[ast.AST], ...]:
        """Return the restricted AST classes.

        Returns:
            AST classes handled by the concrete keyword rule.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def keywords(self) -> tuple[str, ...]:
        """Return the restricted keywords to check for.

        Returns:
            A tuple of restricted keyword strings.

        """
        raise NotImplementedError

    def unpack(self, node: ast.AST) -> str:
        """Extract the value from a node.

        Args:
            node:
                The AST node to extract the value from.

        Returns:
            The value loaded from the node.

        """
        return type(node).__name__.lower()

    def check(self, _: lintkit.Value[typing.Any]) -> bool:
        """Report every loaded value as a rule violation.

        Args:
            _:
                Loaded restricted construct.

        Returns:
            Always ``True`` because loaders yield violations only.

        """
        return True

    def message(self, value: lintkit.Value[str]) -> str:
        """Return a restricted construct violation message.

        Args:
            value:
                Restricted construct name.

        Returns:
            Message describing the restricted construct.

        """
        return f"Avoid restricted keyword: '{value}'"

    def description(self) -> str:
        """Return rule description.

        Returns:
            Rule description string.

        """
        return f"Avoid restricted keywords: {', '.join(self.keywords())}"


class State(_Keyword, lintkit.rule.Node, code=21):
    """Rule checking restricted state management keywords."""

    def ast_classes(
        self,
    ) -> tuple[type[ast.Delete], type[ast.Global], type[ast.Nonlocal]]:
        """Return state management ast_classes.

        Returns:
            (ast.Delete, ast.Global, ast.Nonlocal)

        """
        return (ast.Delete, ast.Global, ast.Nonlocal)

    def keywords(self) -> tuple[str, ...]:
        """Return restricted state management keywords."""
        return ("del", "global", "nonlocal")


class Iteration(_Keyword, lintkit.rule.Node, code=22):
    """Rule checking restricted iteration keywords."""

    def ast_classes(self) -> tuple[type[ast.Break], type[ast.Continue]]:
        """Return forbidden iteration keywords.

        Returns:
            (ast.Break, ast.Continue)

        """
        return (ast.Break, ast.Continue)

    def keywords(self) -> tuple[str, ...]:
        """Return restricted iteration keywords.

        Returns:
            A tuple of restricted iteration keyword strings.

        """
        return ("break", "continue")
