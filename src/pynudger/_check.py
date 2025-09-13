# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Base checks used for multiple rules."""

from __future__ import annotations

import abc
import re
import typing

import lintkit

# Shared functionality


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
        length = self.config.get(f"{self._variable()}_length")  # pyright: ignore[reportAttributeAccessIssue]
        if length is None:
            return 3
        return length  # pragma: no cover

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


class _Regex(lintkit.check.Regex, abc.ABC):
    """Shared regex functionality."""

    def regex_flags(self) -> int:
        """Make the matching case insensitive.

        Returns:
            Flag indicating both upper and lowercase match.

        """
        return re.IGNORECASE


class _What(abc.ABC):
    """What is being avoided."""

    @abc.abstractmethod
    def _what(self) -> str:
        """What is being avoided.

        Returns:
            String describing what is being avoided.

        """
        raise NotImplementedError


class _SetGet(_Regex, _What, abc.ABC):
    """Shared functionality of setters and getters."""

    def message(self, value: lintkit.Value[str]) -> str:
        """Display error message in case of rule violation.

        Args:
            value:
                Value which violated the rule.

        Returns:
            Message describing rule violation.

        """
        goal = re.sub(
            self.regex(),
            "",
            value.__wrapped__,  # pyright: ignore[reportUnknownArgumentType]
            flags=self.regex_flags(),
        )
        if not goal:
            return f"Avoid using {self._what()}."
        return (
            f"Avoid using {self._what()}. Instead of '{value}' "
            f"define '{goal}' as a property."
        )


class _UtilHelperCommon(_Regex, _What, abc.ABC):
    """Shared functionality of utils, helpers and commons."""

    def message(self, _: lintkit.Value[str]) -> str:
        """Display error message in case of rule violation.

        Args:
            _:
                Unused

        Returns:
            Message describing rule violation.

        """
        return (
            f"Avoid defining '{self._what()}'. Use semantically "
            "meaningful names instead."
        )


# Concrete checks


class Set(_SetGet):
    """Match setter and its variations."""

    def regex(self) -> str:
        """Regex matching setters.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"^_?set(?:s|ters?)?_?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "setters" string.

        """
        return "setters"


class Get(_SetGet):
    """Match getter and its variations."""

    def regex(self) -> str:
        """Regex matching getters.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"^_?get(?:s|ters?)?_?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "getters" string.

        """
        return "getters"


class Util(_UtilHelperCommon):
    """Match utilities and its variations."""

    def regex(self) -> str:
        """Regex matching utils.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?util(s|ities)?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "utils" string.

        """
        return "utils"


class Helper(_UtilHelperCommon):
    """Match helpers and its variations."""

    def regex(self) -> str:
        """Regex matching helpers.

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?help(ers?)?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "helpers" string.

        """
        return "helpers"


class Common(_UtilHelperCommon):
    """Match common and its variations."""

    def regex(self) -> str:
        """Regex matching common(s).

        Note:
            It might raise false positives.

        Returns:
            Regex to match

        """
        return r"_?common(s)?"

    def _what(self) -> str:
        """What is being avoided.

        Returns:
            Always "commons" string.

        """
        return "commons"


class Pascal(_Length):
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
        return re.sub(
            "([A-Z][a-z]+)",
            r" \1",
            re.sub(
                "([A-Z]+)",
                r" \1",
                value.__wrapped__,  # pyright: ignore[reportUnknownArgumentType, reportAttributeAccessIssue]
            ),
        ).split()


class Snake(_Length):
    """Calculate length of name based on snake casing."""

    def _variable(self) -> typing.Literal["snake"]:
        """Name of the check.

        Note:
            It is used to display appropriate message.

        Returns:
            Always "snake" string.

        """
        return "snake"

    def _words(self, value: str) -> list[str]:
        """Divide string into words as defined by snake casing.

        Returns:
            List of words

        """
        if value.startswith("__") and value.endswith("__"):
            return value[2:-2].split("_")
        if value.startswith("_"):
            return value[1:].split("_")
        return value.split("_")
