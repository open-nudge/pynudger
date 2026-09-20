# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Expose module-group assignment strategies."""

from __future__ import annotations

from pynudger.rule._optimizer._optimizer import exact, greedy

__all__ = ["exact", "greedy"]
