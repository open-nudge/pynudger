# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules for repeated name words in declarations."""

from __future__ import annotations

import ast
import typing

import lintkit

from pynudger._loader import (
    Class,
    Function,
    GlobalDefinition,
)
from pynudger.rule import _constant

if typing.TYPE_CHECKING:
    import collections.abc


class _Repetition(lintkit.check.Check):
    """Share matching and diagnostics for repeated module names."""

    kind: typing.ClassVar[_constant.Kind]

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
        identifier = "_".join(
            word.casefold()
            for word in self.kind.words(
                value,
                remove_suffix=_constant.Suffix.ERROR
                if self.kind.is_class()
                else None,
            )
        )
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


class RepetitionVariable(_Repetition, GlobalDefinition, code=40):
    """Rule checking module-scope variable binding names."""

    kind: typing.ClassVar[_constant.Kind] = _constant.Kind.VARIABLE

    def values(self) -> collections.abc.Iterable[lintkit.Value[str]]:
        """Yield module-scope variable binding names.

        Yields:
            Variable identifiers with their declaration locations.

        """
        for node in super().nodes():
            if isinstance(node, ast.Name):
                yield lintkit.Value.from_python(node.id, node)


class RepetitionClass(_Repetition, Class, code=41):
    """Rule checking class names in all scopes."""

    kind: typing.ClassVar[_constant.Kind] = _constant.Kind.CLASS


class RepetitionFunction(_Repetition, Function, code=42):
    """Rule checking function names in all scopes."""

    kind: typing.ClassVar[_constant.Kind] = _constant.Kind.FUNCTION
