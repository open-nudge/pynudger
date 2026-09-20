# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Share declaration kinds and name suffixes between rules."""

from __future__ import annotations

import ast
import enum
import typing

from pynudger import error
from pynudger.rule import _words
from pynudger.rule._optimizer import _optimizer

if typing.TYPE_CHECKING:
    import collections.abc

    import lintkit


class Kind(enum.StrEnum):
    """Identify a supported declaration kind."""

    VARIABLE = enum.auto()
    CLASS = enum.auto()
    FUNCTION = enum.auto()

    @classmethod
    def from_node(cls, node: ast.AST) -> Kind:
        """Create a Kind from an AST node.

        Args:
            node: The AST node to classify.

        Returns:
            The Kind corresponding to the node type.
        """
        if isinstance(node, ast.ClassDef):
            return cls.CLASS
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return cls.FUNCTION
        if isinstance(node, (ast.Assign, ast.Name)):
            return cls.VARIABLE

        raise error.UnsupportedNodeError(node)  # pragma: no cover

    def is_class(self) -> bool:
        """Check if this kind represents a class.

        Returns:
            True if this kind is CLASS, False otherwise.
        """
        return self is Kind.CLASS

    def separator(self) -> str:
        """Return the separator used by this declaration kind.

        Returns:
            Empty text for classes or an underscore for other kinds.
        """
        return "" if self.is_class() else "_"

    def words(
        self,
        value: str | lintkit.Value[str],
        remove_suffix: str | None = None,
        exclude_word: str | None = None,
    ) -> list[str]:
        """Split a name into words based on this declaration kind's separator.

        Args:
            value:
                The name to split.
            remove_suffix:
                Suffix to remove from the name before splitting, if any.
            exclude_word:
                Word to exclude from the result, if any.

        Returns:
            A tuple of words.
        """
        if self.is_class():
            return _words.pascal(value, remove_suffix, exclude_word)
        return _words.snake(value, remove_suffix, exclude_word)


class Suffix(enum.StrEnum):
    """Identify a shared name suffix."""

    ERROR = "Error"


class Strategy(enum.StrEnum):
    """Identify a module assignment strategy."""

    GREEDY = enum.auto()
    EXACT = enum.auto()

    def function(
        self,
    ) -> collections.abc.Callable[
        [_optimizer.Options, int], tuple[str | None, ...]
    ]:
        """Return the optimizer function for this strategy.

        Returns:
            The optimizer callable corresponding to this strategy.
        """
        if self == Strategy.EXACT:
            return _optimizer.exact
        if self == Strategy.GREEDY:
            return _optimizer.greedy

        raise error.InvalidStrategyError(self)  # pragma: no cover
