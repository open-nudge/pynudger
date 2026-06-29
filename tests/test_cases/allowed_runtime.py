# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# ruff: noqa: A001, A002

"""Fixture containing allowed annotation-only constructs."""

from __future__ import annotations


def allowed(object: int) -> str:
    """Exercise constructs that should not be runtime violations."""
    value: int = object
    result: str = "value"
    object = value
    _ = object
    return result
