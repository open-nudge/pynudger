# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test clean internal definition rule cases."""
# noqa-file: PYNUDGER43

from __future__ import annotations

import typing


def visible_function() -> None:
    """Define a public function that is small and unused."""


def _used_function() -> int:
    """Return a value from a twice-used internal function.

    Returns:
        A sample integer.
    """
    return 1


used_function_results = (_used_function(), _used_function())


async def visible_async() -> None:
    """Define a public asynchronous function."""


async def _async_used() -> None:
    """Define a twice-used asynchronous function."""


async_results = (_async_used(), _async_used())


class _UsedClass:
    """Define a twice-used internal class."""


first_class = _UsedClass()
second_class = _UsedClass()


class _FiveClass:
    """Define an internal class with five code lines used once.

    Declaration is included in five lines.

    """

    first: int = 1
    second: int = 2
    third: int = 3
    fourth: int = 4


five_class = _FiveClass()


class UsedMethods:
    """Provide a method called twice through self."""

    def _used_method(self) -> int:
        """Return a value from an internal method.

        Returns:
            A sample integer.
        """
        return 1

    def use(self) -> int:
        """Call the internal method twice.

        Returns:
            The sum of two sample integers.
        """
        return self._used_method() + self._used_method()


class UsedClassMethods:
    """Provide a class method called twice through cls."""

    @classmethod
    def _used_cls(cls) -> int:
        """Return a value from an internal class method.

        Returns:
            A sample integer.
        """
        return 1

    @classmethod
    def use(cls) -> int:
        """Call the internal class method twice.

        Returns:
            The sum of two sample integers.
        """
        return cls._used_cls() + cls._used_cls()


class UsedClassName:
    """Provide a method called twice through the class name."""

    def _used_class_name(self) -> int:
        """Return a value from an internal method.

        Returns:
            A sample integer.
        """
        return 1

    def use(self) -> int:
        """Call the internal method twice through its class name.

        Returns:
            The sum of two sample integers.
        """
        return UsedClassName._used_class_name(
            self
        ) + UsedClassName._used_class_name(self)


class AsyncMethods:
    """Provide an asynchronous method called twice through self."""

    async def _async_method(self) -> int:
        """Return a value asynchronously.

        Returns:
            A sample integer.
        """
        return 1

    async def use(self) -> None:
        """Call the internal asynchronous method twice."""
        _ = await self._async_method()
        _ = await self._async_method()


class ReceiverExamples:
    """Show receivers that are not counted as direct method uses."""

    def _target(self) -> int:
        """Define a five-line internal method.

        Returns:
            A sample integer.
        """
        result = 0
        if self:
            return 1
        return result

    def other(self, other: ReceiverExamples) -> int:
        """Call the target through an unrelated receiver.

        Args:
            other:
                Unrelated receiver.

        Returns:
            The result from the unrelated receiver.
        """
        return other._target()

    def parent(self) -> int:
        """Call the target through super.

        Returns:
            The result from the parent implementation.
        """
        return super()._target()  # pyright: ignore[reportAttributeAccessIssue]


class DunderMethods:
    """Define a dunder method excluded from internal method checks."""

    value: int

    def __init__(self) -> None:
        """Initialize the example."""
        self.value = 1


class BlockMethods:
    """Define a method inside a class-level control-flow block."""

    if typing.TYPE_CHECKING:

        def _block_method(self) -> int:
            """Return a value from a block-defined method.

            Returns:
                A sample integer.
            """
            return 1

    def use(self) -> int:
        """Call the block-defined method twice.

        Returns:
            The sum of two sample integers.
        """
        return self._block_method() + self._block_method()


if typing.TYPE_CHECKING:

    def branch_function() -> None:
        """Define a public function in a module-level block."""

    class BranchClass:
        """Define a public class in a module-level block."""


def outer() -> None:
    """Contain definitions that are not module-level candidates."""

    def _nested_function() -> None:
        """Define a nested function."""

    class _NestedClass:  # pyright: ignore[reportUnusedClass]
        """Define a nested class."""

        value: int = 1

    _nested_function()


class NestedMethods:
    """Contain a method with a nested function."""

    def public_method(self) -> None:
        """Contain a nested function that is not a method candidate."""

        def _nested_method() -> None:
            """Define a nested method function."""

        _nested_method()
