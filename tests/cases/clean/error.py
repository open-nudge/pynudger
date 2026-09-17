# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test error suffix handling in class naming rules."""

from __future__ import annotations

from builtins import Exception as ErrorBase


class MyError(ErrorBase):
    """Represent a basic error."""


class RemoteResourceLoadError(ErrorBase):
    """Represent a remote resource loading error."""
