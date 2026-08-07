# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules for repeated module names in identifiers."""

from __future__ import annotations

import abc
import typing

import lintkit

from pynudger._loader import Class, Function, Variable
from pynudger.rule import _words


class _Repetition(
    lintkit.check.Check,
    abc.ABC,
):
    """Share matching and diagnostics for repeated module names."""

    kind: typing.ClassVar[str]

    def check(self, value: lintkit.Value[str]) -> bool:
        """Report identifiers containing the module name as complete words.

        Args:
            value:
                Identifier name to check.

        Returns:
            True when the module name is a non-exact, contiguous word sequence
            in the identifier.
        """
        module_name = self.file.resolve().stem  # pyright: ignore[reportAttributeAccessIssue]
        identifier = "_".join(word.casefold() for word in self._words(value))
        return (
            module_name != identifier
            and f"_{module_name}_" in f"_{identifier}_"
        )

    def message(self, value: lintkit.Value[str]) -> str:
        """Describe the repeated module name.

        Args:
            value:
                Identifier name that repeats the module name.

        Returns:
            Diagnostic message containing both names.
        """
        return (
            f"{self.kind.title()} '{value}' repeats module name "
            f"'{self.file.resolve().stem}'."  # pyright: ignore[reportAttributeAccessIssue]
        )

    def description(self) -> str:
        """Return the public description of the rule.

        Returns:
            Description of the identifier category checked by this rule.
        """
        return f"Avoid repeating module name in {self.kind}."

    @abc.abstractmethod
    def _words(self, value: lintkit.Value[str]) -> list[str]:
        """Split a candidate identifier into matching words.

        Args:
            value:
                Candidate identifier name.

        Returns:
            Words used for module-name matching.
        """
        raise NotImplementedError


class RepetitionVariable(_Repetition, Variable, code=40):
    """Rule checking variable binding names in all scopes."""

    kind: typing.ClassVar[str] = "variable"

    def _words(self, value: lintkit.Value[str]) -> list[str]:
        """Split a variable name using snake_case boundaries."""
        return _words.snake(value)


class RepetitionClass(_Repetition, Class, code=41):
    """Rule checking class names in all scopes."""

    kind: typing.ClassVar[str] = "class"

    def _words(self, value: lintkit.Value[str]) -> list[str]:
        """Split a class name using a raw string required by ``re.sub``."""
        return _words.pascal(
            value.__wrapped__  # pyright: ignore[reportUnknownArgumentType]
        )


class RepetitionFunction(_Repetition, Function, code=42):
    """Rule checking function names in all scopes."""

    kind: typing.ClassVar[str] = "function"

    def _words(self, value: lintkit.Value[str]) -> list[str]:
        """Split a function name using snake-case boundaries."""
        return _words.snake(value)
