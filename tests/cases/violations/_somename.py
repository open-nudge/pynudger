# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test a private module without a matching public object."""

from __future__ import annotations


def _somename() -> None:
    """Expose a private object matching the module name."""


_somename()
_somename()


def files() -> None:
    """Expose an object unrelated to the module name."""
