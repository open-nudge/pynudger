# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test declarations excluded from shared-name reports."""

from __future__ import annotations

import contextlib
import math as excluded_import

user_user = 1
account_value = excluded_import.pi
profile_schema = 1


class LocalOwner:
    """Define a class with an excluded class attribute."""

    local_value: int = 1


def container() -> int:
    """Define local and nested declarations with repeated words.

    Returns:
        The local sample value.
    """
    local_value = 1

    def hidden_account() -> None:
        """Define a nested function."""

    class HiddenAccount:
        """Define a nested class."""

    hidden_account()
    _ = HiddenAccount()
    return local_value


for _excluded_loop in ():
    pass

with contextlib.nullcontext() as excluded_context:
    pass

try:
    attempted_number = account_value
except RuntimeError as excluded_error:
    excluded_error.add_note("ignored")

if excluded_walrus := account_value > 0:
    pass
