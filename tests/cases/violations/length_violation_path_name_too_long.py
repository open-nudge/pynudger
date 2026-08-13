# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for length violations."""
# noqa-file: PYNUDGER43, PYNUDGER46

from __future__ import annotations


class TooLongClassNameThatExceedsNormalLengthExpectations:
    """Dummy loooong class."""


def long_function_with_an_excessively_long_name_to_test_error() -> None:
    """Dummy loooong function."""
