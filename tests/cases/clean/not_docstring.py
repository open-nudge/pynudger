# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test no accidental docstring rule violations."""
# noqa-file: PYNUDGER43

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator


class DocstringExamples:
    """Examples that should not violate docstring rules."""

    def only_self(self) -> None:
        """Method with no real parameters."""

    @classmethod
    def only_cls(cls) -> None:
        """Class method with no real parameters."""


def function_with_args(value: object, **_: dict[str, typing.Any]) -> object:
    """Accept a value.

    Args:
        value:
            Value to accept.
        _:
            Additional keyword arguments.

    Returns:
        Passes through value.

    """
    return value


async def async_with_args(value: object) -> None:
    """Accept a value asynchronously.

    Args:
        value:
            Value to accept.

    """
    _ = value


def generator() -> Iterator[int]:
    """Yield a value.

    Yields:
        A sample value.

    """
    yield 1


def delegated_generator() -> Iterator[int]:
    """Delegate values to another iterable.

    Yields:
        Sample delegated values.

    """
    yield from (1, 2)


async def async_generator() -> AsyncIterator[int]:
    """Yield a value asynchronously.

    Yields:
        A sample asynchronous value.

    """
    yield 1


def return_with_section() -> int:
    """Return a value.

    Returns:
        A sample value.

    """
    return 1


def none_without_returns() -> None:
    """Return annotation does not require a Returns section."""


def missing_annotation():  # noqa: ANN201
    """Missing return annotation does not require a Returns section."""
    return 1


def outer_nested() -> None:
    """Outer function does not own the nested yield."""

    def nested_generator() -> Iterator[int]:
        """Nested generator owns the yield.

        Yields:
            A nested value.

        """
        yield 1

    _ = nested_generator
