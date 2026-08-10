# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test pipe type unions at the limit and runtime bitwise operations."""

from __future__ import annotations

type Trio = int | str | bytes
type Reused = Trio | float | complex
type Bounded[T: int | str | bytes] = list[T]
first, second, third, fourth = 1, 2, 4, 8
flags = first | second | third | fourth
