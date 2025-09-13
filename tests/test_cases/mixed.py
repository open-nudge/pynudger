# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Module containing class which should raise mixed errors."""

from __future__ import annotations


class SetMixedClassTooLong:
    """Dummy class mixing multiple errors."""

    def __special_long_method_bad_name__(self) -> None:
        """Dummy special long method bad name."""

    def _get_hidden_method_too_long_name(self) -> None:
        """Dummy hidden method too long name."""
