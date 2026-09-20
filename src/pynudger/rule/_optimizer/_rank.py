# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rank exact assignments and greedy groups."""

from __future__ import annotations

import dataclasses
import math
import typing

if typing.TYPE_CHECKING:
    import collections


@dataclasses.dataclass(frozen=True, order=True)
class Assignment:
    """Order exact assignments by coverage, privacy, groups, and names."""

    assigned: float = math.inf
    private: float = math.inf
    groups: float = math.inf
    lexical: tuple[tuple[bool, str], ...] = ()

    @classmethod
    def from_choice(
        cls,
        *,
        choice: tuple[str | None, ...],
        counts: collections.Counter[str],
    ) -> Assignment:
        """Rank one valid assignment.

        Args:
            choice: Target stem for each declaration.
            counts: Number of declarations assigned to each target.

        Returns:
            Ordered score for the assignment.
        """
        used = tuple(stem for stem in choice if stem is not None)
        return cls(
            assigned=-len(used),
            private=-sum(stem.startswith("_") for stem in used),
            groups=len(counts),
            lexical=tuple((stem is None, stem or "") for stem in choice),
        )

    def worse(self, other: Assignment) -> bool:
        """Report whether this rank loses to another rank.

        Args:
            other: Rank to compare.

        Returns:
            True when the other rank is better.
        """
        return self > other


@dataclasses.dataclass(frozen=True, order=True)
class Group:
    """Order greedy groups by size, privacy, and name."""

    count: int
    public: bool
    stem: str

    @classmethod
    def from_count(cls, *, stem: str, count: int) -> Group:
        """Rank a group with its declaration count.

        Args:
            stem: Target module stem.
            count: Number of eligible declarations.

        Returns:
            Ordered score for the group.
        """
        return cls(-count, not stem.startswith("_"), stem)
