# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

import abc
import typing

import lintkit

from pynudger._loader import Class, Function, Path
from pynudger.rule import _words


class _Length(lintkit.check.Check, abc.ABC):
    """Calculate length of the value."""

    @abc.abstractmethod
    def _variable(self) -> str:
        """Name of the check.

        Note:
            It is used to display appropriate message.

        Returns:
            Appropriate name of the length subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def _words(self, value: str) -> list[str]:
        """Divide string into words as defined by concrete class.

        Returns:
            List of words

        """
        raise NotImplementedError

    def check(self, value: lintkit.Value[str]) -> bool:
        """Verify if the length of the value exceeds the limit.

        Args:
            value:
                Value which is unpacked (ast.AST node or path changed
                    to string)

        Returns:
            True if the length exceeds the limit, False otherwise.

        """
        words = self._words(value)
        to_exclude: list[str] = self.config.get(  # pyright: ignore[reportAttributeAccessIssue]
            f"{self._variable()}_excludes", []
        )
        for word in to_exclude:
            if word.lower() in words:  # pragma: no cover
                words.remove(word)  # pyright: ignore[reportUnknownArgumentType]

        return len(words) > self._length()

    def _length(self) -> int:
        """Get length limit from config or return default.

        Returns:
            Length limit

        """
        return self.config.get(f"{self._variable()}_length", 3)  # pyright: ignore[reportAttributeAccessIssue]

    def message(self, value: lintkit.Value[str]) -> str:
        """Display error message in case of rule violation.

        Args:
            value:
                Value which violated the rule.

        Returns:
            Message describing rule violation.

        """
        return (
            f"'{value}' has too many words (maximum: {self._length()}). "
            "Consider using modules and submodules instead."
        )

    def description(self) -> str:
        """Return rule description."""
        kind = type(self).__name__.lower()
        return f"Avoid long {kind} names. Specify intent by nesting modules/packages."


class _Pascal(_Length):
    """Calculate length of name based on pascal casing."""

    def _variable(self) -> typing.Literal["pascal"]:
        """Name of the check.

        Note:
            It is used to display appropriate message.

        Returns:
            Always "pascal" string.

        """
        return "pascal"

    def _words(self, value: str) -> list[str]:
        """Divide string into words as defined by pascal casing.

        Returns:
            List of words

        """
        return _words.pascal(value)


class _Snake(_Length):
    """Calculate length of name based on snake casing."""

    def _variable(self) -> typing.Literal["snake"]:
        """Name of the check.

        Note:
            It is used to display appropriate message.

        Returns:
            Always "snake" string.

        """
        return "snake"

    def _words(self, value: str) -> list[str]:  # pragma: no cover
        """Divide string into words as defined by snake casing.

        Returns:
            List of words

        """
        return _words.snake(value)


# Length rules
class LengthClass(_Pascal, Class, code=18):
    """Rule for checking class's name length (word-wise)."""


class LengthFunction(_Snake, Function, code=19):
    """Rule for checking function's name length (word-wise)."""


class LengthPath(_Snake, Path, code=20):
    """Rule for checking path name length (word-wise)."""
