# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules validating calls."""

from __future__ import annotations

import abc
import typing

import lintkit

from pynudger._loader import Call


class _Keywords(lintkit.check.Check, abc.ABC):
    """Check values loaded only when a restricted construct was found."""

    def check(self, value: lintkit.Value[typing.Any]) -> bool:
        """Report every loaded value as a rule violation.

        Args:
            value:
                Possible offending value.

        Returns:
            True if value is in the restricted keywords.

        """
        if not hasattr(self, "_keywords"):
            # Cache in class itself as these are unchange'able
            type(self)._keywords = self.keywords()  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]

        return value in self._keywords  # pyright: ignore[reportAttributeAccessIssue]

    @abc.abstractmethod
    def topic(self) -> str:
        """Return the restricted construct group name.

        Returns:
            Human-readable group name.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def keywords(self) -> tuple[str, ...]:
        """Return restricted keyword names.

        Returns:
            Restricted keyword names checked by the rule.

        """
        raise NotImplementedError

    def message(self, value: lintkit.Value[str]) -> str:
        """Return a restricted construct violation message.

        Args:
            value:
                Restricted construct name.

        Returns:
            Message describing the restricted construct.

        """
        return f"Avoid restricted {self.topic()}: '{value}'."

    def description(self) -> str:
        """Return rule description."""
        return f"Avoid restricted {self.topic()}: {','.join(self.keywords())}."


class Compatibility(
    _Keywords,
    Call,
    code=23,
):
    """Rule checking restricted Python 2 compatibility functions."""

    def topic(self) -> str:
        """Return rule topic."""
        return "compatibility functions"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("object", "basestring", "unicode", "long")


class Interactive(
    _Keywords,
    Call,
    code=24,
):
    """Rule checking restricted utility and interactive functions."""

    def topic(self) -> str:
        """Return rule topic."""
        return "utility/interactive functions"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("help", "breakpoint")


class Cast(_Keywords, Call, lintkit.rule.Node, code=25):
    """Rule checking restricted explicit casting functionality."""

    def topic(self) -> str:
        """Return rule topic."""
        return "explicit casting functionality"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("typing.cast", "cast", "bool", "float", "int", "str")


class Insecure(_Keywords, Call, lintkit.rule.Node, code=26):
    """Rule checking restricted insecure builtin functions."""

    def topic(self) -> str:
        """Return rule topic."""
        return "insecure builtin functions"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("exec", "eval", "compile")


class Iteration(_Keywords, Call, lintkit.rule.Node, code=27):
    """Rule checking restricted explicit iteration functions."""

    def topic(self) -> str:
        """Return rule topic."""
        return "explicit iteration"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("iter", "aiter", "anext", "next")


class Attribute(
    _Keywords,
    Call,
    lintkit.rule.Node,
    code=28,
):
    """Rule checking restricted attribute manipulation functionality."""

    def topic(self) -> str:
        """Return rule topic."""
        return "attribute manipulation"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return (
            "delattr",
            "getattr",
            "hasattr",
            "setattr",
            "globals",
            "locals",
            "vars",
            "dir",
        )
