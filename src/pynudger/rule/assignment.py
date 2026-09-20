# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Assign module-scope declarations to shared-name modules."""

from __future__ import annotations

import ast
import dataclasses
import typing

import lintkit

from pynudger._loader import GlobalDefinition
from pynudger.rule import _constant

if typing.TYPE_CHECKING:
    import collections.abc

    from pynudger import _types


class Name(lintkit.check.Check, GlobalDefinition, code=43):
    """Rule checking shared words in module-scope declaration names.

    TLDR:
        1. Collect eligible module-scope declarations.
        2. Split names and omit class `Error` suffixes from target choices.
        3. Add private targets and omit the source module.
        4. Select valid groups by exact or greedy assignment.
        5. Emit at most one suggestion per assigned declaration.

    `PYNUDGER43` suggests a move only when a target module has at least
    `minimum_same_name_occurrences` assigned declarations. Exact assignment
    is the default and can take exponential time when names have many
    overlapping target choices.

    Set `assignment_strategy = "greedy"` under
    `[tool.pynudger.PYNUDGER43]` for faster grouping that may report fewer
    declarations.

    """

    def values(self) -> collections.abc.Iterable[lintkit.Value[_Candidate]]:
        """Assign declarations to valid groups in source order.

        Yields:
            One diagnostic candidate for each assigned declaration.

        """
        minimum: int = self.config("minimum_same_name_occurrences", 2)
        configured: str = self.config("assignment_strategy", "exact")
        strategy = _constant.Strategy(configured)
        yield from _candidates(
            super().nodes(),
            self.file.resolve().stem,
            minimum,
            strategy,
        )

    def check(self, value: lintkit.Value[_Candidate]) -> bool:
        """Accept a candidate from a group that meets the minimum.

        Args:
            value:
                Candidate assigned by the optimizer.

        Returns:
            True because the optimizer only returns valid groups.
        """
        return bool(value.stem)

    def message(self, value: lintkit.Value[_Candidate]) -> str:
        """Describe the target path and proposed declaration name.

        Args:
            value:
                Assigned declaration and its target.

        Returns:
            Diagnostic with the target path and proposed name.
        """
        target = self.file.resolve().with_suffix("") / f"{value.stem}.py"
        return (
            f"{value.label} '{value.name}' should be placed under module "
            f"'{target}' as '{value.renamed}'."
        )

    def description(self) -> str:
        """Return the public rule description.

        Returns:
            Description of the module-grouping rule.
        """
        return "Group globals with shared name words under modules."


@dataclasses.dataclass(frozen=True)
class _Declaration:
    """Keep one name and its raw, eligible tokens."""

    name: str
    kind: _constant.Kind
    tokens: list[str]
    group_tokens: list[str]
    private: bool

    @classmethod
    def from_name(cls, name: str, kind: _constant.Kind) -> _Declaration:
        """Build declaration details from a name and kind.

        Args:
            name:
                Module-scope declaration name.
            kind:
                Declaration kind.

        Returns:
            Name, kind, and tokens for the declaration.
        """
        tokens = kind.words(name.removeprefix("_"))

        group_tokens = (
            tokens[:-1]
            if tokens
            and kind.is_class()
            and tokens[-1] == _constant.Suffix.ERROR
            else tokens
        )
        return cls(name, kind, tokens, group_tokens, name.startswith("_"))


@dataclasses.dataclass(frozen=True)
class _Candidate:
    """Keep the diagnostic fields for one assigned declaration."""

    name: str
    label: str
    stem: str
    renamed: str


def _candidates(
    nodes: collections.abc.Iterable[_types.GlobalDefinitionNode],
    module: str,
    minimum: int,
    strategy: _constant.Strategy,
) -> collections.abc.Iterable[lintkit.Value[_Candidate]]:
    """Pair assigned names with their source nodes.

    Args:
        nodes:
            Module-scope declaration nodes in source order.
        module:
            Source module stem.
        minimum:
            Minimum size of an assigned group.
        strategy:
            Assignment strategy.

    Yields:
        One lintkit value for each assigned declaration.
    """
    source_nodes = tuple(nodes)
    names = tuple(
        (
            node.id if isinstance(node, ast.Name) else node.name,
            _constant.Kind.from_node(node),
        )
        for node in source_nodes
    )
    for node, candidate in zip(
        source_nodes,
        _raw_candidates(names, module, minimum, strategy),
        strict=True,
    ):
        if candidate is not None:
            yield lintkit.Value.from_python(candidate, node)


def _raw_candidates(
    names: collections.abc.Sequence[tuple[str, _constant.Kind]],
    module: str,
    minimum: int,
    strategy: _constant.Strategy,
) -> tuple[_Candidate | None, ...]:
    """Assign names to target modules in input order.

    Args:
        names:
            Declaration names and kinds in source order.
        module:
            Source module stem to exclude from target choices.
        minimum:
            Minimum size of an assigned group.
        strategy:
            Exact or greedy assignment strategy.

    Returns:
        One candidate or None for each input name.
    """
    source = module.casefold()
    declarations = tuple(
        _Declaration.from_name(name, kind) for name, kind in names
    )
    options: list[tuple[str, ...]] = []

    for declaration in declarations:
        stems = {
            token.casefold() for token in declaration.group_tokens if token
        }
        if declaration.private:
            stems.update({f"_{stem}" for stem in stems})
        options.append(
            tuple(sorted(stems - {source}))
            if not declaration.name.startswith("__")
            else ()
        )

    return tuple(
        _Candidate(
            declaration.name,
            declaration.kind.title(),
            stem,
            _rename(declaration, stem),
        )
        if stem is not None
        else None
        for declaration, stem in zip(
            declarations, strategy.function()(options, minimum), strict=True
        )
    )


def _rename(declaration: _Declaration, stem: str) -> str:
    """Remove each selected raw token and retain a usable name.

    Args:
        declaration:
            Declaration with raw and eligible tokens.
        stem:
            Selected target module stem.

    Returns:
        Proposed declaration name in the target module.
    """
    word = stem.removeprefix("_")
    remaining = [
        token for token in declaration.group_tokens if token.casefold() != word
    ]
    remaining.extend(declaration.tokens[len(declaration.group_tokens) :])
    separator = declaration.kind.separator()
    body = separator.join(remaining) or declaration.name.removeprefix("_")
    prefix = "_" if declaration.private and not stem.startswith("_") else ""
    return prefix + body
