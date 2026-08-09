# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test declarations that share one case-insensitive name word."""

from __future__ import annotations

account_value = 1  # noqa: PYNUDGER43


class _AccountModel:  # noqa: PYNUDGER38, PYNUDGER43
    """Define an internal class sharing the account word."""


_ = _AccountModel()


def build_account() -> None:
    """Define a function sharing the account word."""
