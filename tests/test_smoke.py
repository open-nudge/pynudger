# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests of the package."""

from __future__ import annotations

import pynudger


def test_version() -> None:
    """Smoke test package version."""
    # nosemgrep
    assert pynudger.__version__ != ""
