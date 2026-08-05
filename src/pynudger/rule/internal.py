# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules for small and rarely used internal definitions."""

from __future__ import annotations

import typing

import lintkit

from pynudger.rule import _internal

if typing.TYPE_CHECKING:
    import ast
    import collections.abc


class _Internal(
    lintkit.check.Check,
    lintkit.loader.Python,
    lintkit.rule.Node,
):
    """Shared rule implementation for internal definitions."""

    kind: typing.ClassVar[str]

    def values(
        self,
    ) -> collections.abc.Iterable[lintkit.Value[_internal.Candidate]]:
        """Yield every internal candidate of this rule's definition type.

        Yields:
            ``lintkit.Value[_internal.Candidate]`` objects for internal
            candidates only.

        """
        tree: ast.Module = self.getitem("ast")
        lines = self.content.splitlines()  # pyright: ignore[reportOptionalMemberAccess]
        for candidate in _internal.candidates(tree, lines, self.kind):
            yield lintkit.Value.from_python(candidate, candidate.node)

    def check(self, value: lintkit.Value[_internal.Candidate]) -> bool:
        """Report internal candidates below both configured thresholds.

        Args:
            value:
                ``lintkit.Value`` wrapping the candidate record to check.

        Returns:
            ``True`` when usage is below its minimum and code lines are below
            their minimum.
        """
        minimum_usages, minimum_lines = self._limits()
        return (
            value.usage_count < minimum_usages
            and value.code_lines < minimum_lines
        )

    def description(self) -> str:
        """Return the human-readable description of this rule.

        Returns:
            Rule description containing the definition category and usage
            threshold.
        """
        minimum_usages, minimum_lines = self._limits()
        return (
            f"Report internal {self.kind} definitions with fewer than "
            f"'{minimum_usages}' usages and {minimum_lines} code lines."
        )

    def message(self, value: lintkit.Value[_internal.Candidate]) -> str:
        """Return a message with candidate metrics and configured limits.

        Args:
            value:
                ``lintkit.Value`` wrapping the candidate that violated the
                rule.

        Returns:
            Message describing the candidate and both threshold values.
        """
        minimum_usages, minimum_lines = self._limits()
        return (
            f"Internal {self.kind} '{value.name}' has "
            f"{value.usage_count} usages and {value.code_lines} code lines; "
            f"configured minimums are {minimum_usages} usages and "
            f"{minimum_lines} code lines."
        )

    def _limits(self) -> tuple[int, int]:
        """Return configured minimum usage and code-line thresholds.

        Returns:
            A ``(minimum_usages, minimum_lines)`` tuple. Missing configuration
            values default to two usages and five code lines.
        """
        minimum_usages = self.config.get(  # pyright: ignore[reportAttributeAccessIssue]
            f"minimum_internal_{self.kind}_usages", 2
        )
        minimum_lines = self.config.get(  # pyright: ignore[reportAttributeAccessIssue]
            f"minimum_internal_{self.kind}_lines", 5
        )
        return minimum_usages, minimum_lines


class InternalFunction(_Internal, code=37):
    """Rule checking module-level synchronous and asynchronous functions."""

    kind: typing.ClassVar[str] = "function"


class InternalClass(_Internal, code=38):
    """Rule checking module-level classes."""

    kind: typing.ClassVar[str] = "class"


class InternalMethod(_Internal, code=39):
    """Rule checking methods of module-level classes."""

    kind: typing.ClassVar[str] = "method"
