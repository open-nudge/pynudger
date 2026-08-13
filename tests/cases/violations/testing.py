# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Module testing multiple assert rule violations."""

# noqa-file: PYNUDGER46

from __future__ import annotations


def test_count() -> None:
    """Use too many assert statements."""
    # nosemgrep
    assert True
    # nosemgrep
    assert True
