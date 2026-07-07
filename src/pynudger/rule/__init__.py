# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Public API for the pynudger rule system.

Submodules are re-exported to utilize side effects of rule registration
as done by `lintkit`.

"""

from __future__ import annotations

from pynudger.rule import (
    attribute,
    call,
    common,
    getter,
    helper,
    keyword,
    length,
    setter,
    string,
    testing,
    util,
)

__all__ = [
    "attribute",
    "call",
    "common",
    "getter",
    "helper",
    "keyword",
    "length",
    "setter",
    "string",
    "testing",
    "util",
]
