# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: B009, I001, PIE790, PLW0603, S307, T100, TC006, UP004

"""Fixture containing restricted runtime constructs."""

from __future__ import annotations

import asyncio
import typing


global_value = None


class Legacy(object):
    """Compatibility base fixture."""

    pass


def control(value: typing.Any) -> None:
    """Exercise state and iteration keyword restrictions."""
    global global_value
    global_value = value
    enclosing = value
    del value

    def closure() -> None:
        nonlocal enclosing
        enclosing = global_value

    closure()
    for item in (enclosing,):
        global_value = item
        continue
    for item in (global_value,):
        global_value = item
        break


def calls(value: typing.Any) -> None:
    """Exercise runtime call and attribute restrictions."""
    breakpoint()
    _ = (
        typing.cast(int, value),
        object(),
        eval("value"),
        iter((value,)),
        getattr(value, "name"),
        value.__dict__,
    )


class Attributes:
    """Attribute decorator fixture."""

    @property
    def value(self) -> typing.Any:
        """Return fixture value."""
        return self.__dict__

    @property
    async def async_value(self) -> typing.Any:
        """Return asynchronous fixture value."""
        await asyncio.sleep(0)
        return self.__dict__
