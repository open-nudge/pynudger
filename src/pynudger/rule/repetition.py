# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules for repeated name words in declarations."""

from __future__ import annotations

import ast
import collections
import collections.abc
import dataclasses
import typing

import lintkit

from pynudger._loader import (
    Class,
    Function,
    GlobalDefinition,
    Variable,
)
from pynudger.rule import _words

if typing.TYPE_CHECKING:
    from pynudger._loader import GlobalDefinitionNode


class _Repetition(lintkit.check.Check):
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
        identifier = "_".join(
            word.casefold() for word in _split(self.kind, value)
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


class RepetitionVariable(_Repetition, Variable, code=40):
    """Rule checking variable binding names in all scopes."""

    kind: typing.ClassVar[str] = "variable"


class RepetitionClass(_Repetition, Class, code=41):
    """Rule checking class names in all scopes."""

    kind: typing.ClassVar[str] = "class"


class RepetitionFunction(_Repetition, Function, code=42):
    """Rule checking function names in all scopes."""

    kind: typing.ClassVar[str] = "function"


@dataclasses.dataclass(frozen=True)
class _Candidate:
    """Represent one declaration word and its module-wide frequency."""

    node: GlobalDefinitionNode
    word: str
    occurrences: int


class Name(
    lintkit.check.Check,
    GlobalDefinition,
    code=43,
):
    """Rule checking shared words in module-scope declaration names."""

    def values(
        self,
    ) -> collections.abc.Iterable[lintkit.Value[_Candidate]]:
        """Yield every declaration-word candidate with its total count.

        Yields:
            Every unique declaration-word pair with the word's module-wide
            occurrence count.

        """
        candidates = [
            candidate
            for node in super().nodes()
            for candidate in self._split_node(node)
        ]
        counts = collections.Counter(word for _, word in candidates)
        for node, word in candidates:
            candidate = _Candidate(node, word, counts[word])
            yield lintkit.Value.from_python(candidate, node)

    def check(self, value: lintkit.Value[_Candidate]) -> bool:
        """Report candidates meeting the configured occurrence minimum.

        Args:
            value:
                Declaration-word candidate with its module-wide count.

        Returns:
            Whether the candidate reaches the configured minimum.

        """
        return value.occurrences >= self.config.get(  # pyright: ignore[reportAttributeAccessIssue]
            "minimum_same_name_occurrences", 2
        )

    def message(self, value: lintkit.Value[_Candidate]) -> str:
        """Describe the module that should own the declaration.

        Args:
            value:
                Repeated declaration-word candidate.

        Returns:
            Diagnostic with the declaration kind, name, and module name.

        """
        node = typing.cast("GlobalDefinitionNode", value.node)
        name = node.id if isinstance(node, ast.Name) else node.name
        return (
            f"{self._label(node)} '{name}' should be placed under module "
            f"'{value.word}'."
        )

    def description(self) -> str:
        """Return the public rule description.

        Returns:
            Description of the module-grouping rule.

        """
        return "Group globals with shared name words under modules."

    def _split_node(
        self,
        node: GlobalDefinitionNode,
    ) -> tuple[tuple[GlobalDefinitionNode, str], ...]:
        """Split one declaration into unique normalized word candidates.

        Args:
            node:
                Supported module-scope declaration.

        Returns:
            One candidate for each unique declaration word.

        """
        name = node.id if isinstance(node, ast.Name) else node.name
        words = _split(
            kind="class" if isinstance(node, ast.ClassDef) else "", value=name
        )
        normalized = (word.casefold() for word in words)
        return tuple((node, word) for word in set(normalized))

    @staticmethod
    def _label(node: GlobalDefinitionNode) -> str:  # pragma: no cover
        """Return the human-readable declaration kind.

        Args:
            node:
                Declaration node to classify.

        Returns:
            Variable, class, or function label.

        """
        if isinstance(node, ast.Name):
            return "Variable"
        if isinstance(node, ast.ClassDef):
            return "Class"
        return "Function"


def _split(kind: str, value: str | lintkit.Value[str]) -> list[str]:
    """Split a declaration name according to its kind.

    Args:
        kind:
            Declaration kind selecting PascalCase or snake_case splitting.
        value:
            Declaration name or its diagnostic proxy.

    Returns:
        Words used by repetition and shared-name rules.

    """
    if kind == "class":
        return _words.pascal(value)
    return _words.snake(value)
