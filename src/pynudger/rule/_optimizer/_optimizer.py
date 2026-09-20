# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Assign declarations to module stems without depending on syntax trees."""

from __future__ import annotations

import collections
import collections.abc
import itertools

from pynudger.rule._optimizer import _rank

type Options = collections.abc.Sequence[collections.abc.Sequence[str]]


def exact(options: Options, minimum: int) -> tuple[str | None, ...]:
    """Find the best assignment with no search-size limit.

    Args:
        options:
            Eligible target stems for declarations in source order.
        minimum:
            Minimum number of declarations in each used group.

    Returns:
        One target stem or None for each declaration.
    """
    best: tuple[str | None, ...] = (None,) * len(options)
    best_rank = _rank.Assignment()

    # Add None to each declaration's choices, then enumerate every assignment.
    for choice in itertools.product(*((*row, None) for row in options)):
        counts = collections.Counter(
            stem for stem in choice if stem is not None
        )
        if all(count >= minimum for count in counts.values()):
            rank = _rank.Assignment.from_choice(choice=choice, counts=counts)
            if best_rank.worse(rank):
                best, best_rank = choice, rank

    return best


def greedy(options: Options, minimum: int) -> tuple[str | None, ...]:
    """Assign each largest valid group until no valid group remains.

    Args:
        options:
            Eligible target stems for declarations in source order.
        minimum:
            Minimum number of declarations in each used group.

    Returns:
        One target stem or None for each declaration.
    """
    assigned: list[str | None] = [None] * len(options)
    remaining = set(range(len(options)))

    while remaining:
        counts = collections.Counter(
            stem for index in remaining for stem in set(options[index])
        )
        group = min(
            (
                _rank.Group.from_count(stem=stem, count=count)
                for stem, count in counts.items()
                if count >= minimum
            ),
            default=None,
        )
        if group is None:
            return tuple(assigned)
        stem = group.stem
        selected = {index for index in remaining if stem in options[index]}
        for index in selected:
            assigned[index] = stem
        remaining.difference_update(selected)

    return tuple(assigned)
