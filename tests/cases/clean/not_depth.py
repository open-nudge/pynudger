# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test types at or below the default subscript depth limit."""

from __future__ import annotations

import typing

integer: int
sequence: list  # pyright: ignore[reportMissingTypeArgument]
dictionary: dict  # pyright: ignore[reportMissingTypeArgument]
bespoke: Custom  # noqa: F821  # pyright: ignore[reportUndefinedVariable]
elements: list[int]
parameterized: Custom[int]  # noqa: F821  # pyright: ignore[reportUndefinedVariable]
pairs: dict[str, int]
maybe: typing.Optional[int]  # noqa: UP045  # pyright: ignore[reportDeprecated]
nullable: int | None
type Items = list[int]
wrapped: list[Items]
quoted: "list[list[int]]"  # noqa: UP037
