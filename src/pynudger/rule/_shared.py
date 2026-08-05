# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared rules functionality."""

from __future__ import annotations

import abc
import re

import lintkit


class Regex(lintkit.check.Regex, abc.ABC):
    """Shared regex functionality."""

    def regex_flags(self) -> int:
        """Make the matching case insensitive.

        Returns:
            Flag indicating both upper and lowercase match.

        """
        return re.IGNORECASE


class What(abc.ABC):
    """What is being avoided."""

    @abc.abstractmethod
    def _what(self) -> str:
        """What is being avoided.

        Returns:
            String describing what is being avoided.

        """
        raise NotImplementedError

    def description(self) -> str:
        """Return rule description."""
        kind = type(self).__name__.lower()
        return f"Avoid using {self._what()} in {kind} names. Name the {kind} appropriately."


class SetGet(Regex, What, abc.ABC):
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


class UtilHelperCommon(Regex, What, abc.ABC):
    """Shared functionality of utils, helpers, commons, and shared names."""

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
