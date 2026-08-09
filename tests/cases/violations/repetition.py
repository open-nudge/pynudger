# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test repeated module-name violations."""
# noqa-file: PYNUDGER43

from __future__ import annotations

repetition_global = 1


class RepetitionClass:
    """Use a class name that repeats the module name."""


async def repetition_function() -> None:
    """Use an asynchronous function name that repeats the module name."""
